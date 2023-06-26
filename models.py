from typing import Any
import mesa
import random
from agents import Ant, Colony, Food, Pheromone
from mesa.visualization.modules import CanvasGrid

GRID_SIZE = 15

class AntColonyModel(mesa.Model):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)

    self.grid = mesa.space.MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = mesa.time.RandomActivation(self)
    self.current_step = 0

    colony = Colony(-1, self, 0)
    self.grid.place_agent(
      colony,
      (self._get_grid_center()['x'], self._get_grid_center()['y'])
    )
    self.schedule.add(colony)

    for i in range(5):
      ant = Ant(i, self)
      x = self.random.randrange(self._get_grid_center()['x'] - 5, self._get_grid_center()['x'] + 5)
      y = self.random.randrange(self._get_grid_center()['y'] - 5, self._get_grid_center()['y'] + 5)
      self.grid.place_agent(ant, (x, y))
      self.schedule.add(ant)

    for _ in range(5):
      self._spawn_food_at_random_location()

  def _get_grid_center(self) -> dict:
    return { 'x': self.grid.width // 2, 'y': self.grid.height // 2 }

  def _spawn_food_at_random_location(self) -> None:
    food = Food(self._last_agent_id() + 1, self, random.randrange(25, 50))
    x = self.random.randrange(self.grid.width)
    y = self.random.randrange(self.grid.height)
    self.grid.place_agent(food, (x, y))
    self.schedule.add(food)

  def _last_agent_id(self) -> int:
    return max(self.schedule._agents.keys())

  def step(self) -> None:
    self.current_step += 1
    if self.current_step % 5 == 0:
      self._spawn_food_at_random_location()

    self.schedule.step()

def agent_portrayal(agent: mesa.Agent) -> dict:
  if agent is None:
    return {}
  
  portrayal = {}

  if type(agent) is Colony:
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 2
    portrayal["Color"] = "blue"
    portrayal["r"] = 1.0
  elif type(agent) is Ant:
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 1
    if agent.state == "searching":
      portrayal["Color"] = "black"
    else:
      portrayal["Color"] = "red"
    portrayal["r"] = 0.5
  elif type(agent) is Food:
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["Color"] = "green"
    portrayal["r"] = 0.35
  elif type(agent) is Pheromone:
    c = agent.steps_valid
    portrayal["Shape"] = "rect"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["Color"] = f"#50{c}050"
    portrayal["w"] = 1
    portrayal["h"] = 1

  return portrayal

canvas = CanvasGrid(agent_portrayal, GRID_SIZE, GRID_SIZE, 500, 500)
server = mesa.visualization.ModularServer(AntColonyModel, [canvas], "Ant Colony Model")
server.port = 8521
server.launch()