import random
import mesa
from mesa.model import Model

class AntState:
  SEARCHING = "searching"
  RETURNING = "returning"

class Ant(mesa.Agent):
  def __init__(self, unique_id: int, model: mesa.Model) -> None:
    super().__init__(unique_id, model)

    self.state: str = AntState.SEARCHING

  def step(self) -> None:
    if self.state == AntState.SEARCHING:
      self.move_search()
      self.grab_food()
    else:
      self.move_return()

  def move_return(self) -> None:
    center = self.model.grid.width // 2, self.model.grid.height // 2

    if self.pos == center:
      self.state = AntState.SEARCHING
      return
    
    dx = center[0] - self.pos[0]
    dy = center[1] - self.pos[1]
    unit_vector = dx // max(1, abs(dx)), dy // max(1, abs(dy))

    next_pos = self.pos[0] + unit_vector[0], self.pos[1] + unit_vector[1]
    self.model.grid.move_agent(self, next_pos)

  def move_search(self) -> None:
    possible_steps = self.model.grid.get_neighborhood(
      self.pos,
      moore=True,
      include_center=False
    )

    neighbours = self.model.grid.get_cell_list_contents(possible_steps)
    busy_cells = [cell for cell in possible_steps if cell not in self.model.grid.empties]
    empty_cells = [cell for cell in possible_steps if cell in self.model.grid.empties]

    next_pos = random.choice(empty_cells)

    if len(neighbours) > 0:
      food = [obj for obj in neighbours if isinstance(obj, Food)]
      if len(food) > 0:
        food_to_eat = random.choice(food)
        next_pos = food_to_eat.pos
        
    self.model.grid.move_agent(self, next_pos)

    for cell in busy_cells:
      cellmates = self.model.grid.get_cell_list_contents([cell])
      if len(cellmates) > 0:
        food = [obj for obj in cellmates if isinstance(obj, Food)]
        if len(food) > 0:
          self.model.grid.move_agent(self, cell)
          return

  def grab_food(self) -> None:
    food_to_grab = [obj for obj in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(obj, Food)]
    if len(food_to_grab) > 0:
      print("Food grabbed", food_to_grab[0].unique_id)
      food_to_grab[0].grabbed = True
      self.state = AntState.RETURNING

class Food(mesa.Agent):
  def __init__(self, unique_id: int, model: mesa.Model, steps_valid: int) -> None:
    super().__init__(unique_id, model)

    self.steps_valid = steps_valid
    self.grabbed = False

  def step(self) -> None:
    if self.grabbed:
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)


    if self.steps_valid <= 0:
      self.model.grid.remove_agent(self)
      self.model.schedule.remove(self)
    else:
      self.steps_valid -= 1

class Colony(mesa.Agent):
  def __init__(self, unique_id: int, model: Model, start_food: int) -> None:
    super().__init__(unique_id, model)
    
    self.stored_food = start_food

  def step(self) -> None:
    pass