import random
import mesa

class Ant(mesa.Agent):
  def __init__(self, unique_id: int, model: mesa.Model) -> None:
    super().__init__(unique_id, model)

  def step(self) -> None:
    self.move()
    # self.eat()
    # self.reproduce()

  def move(self) -> None:
    possible_steps = self.model.grid.get_neighborhood(
      self.pos,
      moore=True,
      include_center=False
    )
    new_position = random.choice(possible_steps)
    self.model.grid.move_agent(self, new_position)

class Food(mesa.Agent):
  def __init__(self, unique_id: int, model: mesa.Model) -> None:
    super().__init__(unique_id, model)
