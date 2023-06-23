from typing import Any
import mesa
import random
from agents import Ant, Food
from mesa.visualization.modules import CanvasGrid

GRID_SIZE = 50

class AntFarmModel(mesa.Model):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)

    self.grid = mesa.space.MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = mesa.time.SimultaneousActivation(self)
    self.current_step = 0

    for i in range(20):
      ant = Ant(i, self)
      x = self.random.randrange(self._get_grid_center()['x'] - 10, self._get_grid_center()['x'] + 10)
      y = self.random.randrange(self._get_grid_center()['y'] - 10, self._get_grid_center()['y'] + 10)
      self.grid.place_agent(ant, (x, y))
      self.schedule.add(ant)

    for _ in range(10):
      self._spawn_food_at_random_location()

  def _get_grid_center(self) -> dict:
    return { 'x': self.grid.width / 2, 'y': self.grid.height / 2 }

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

  if type(agent) is Ant:
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["Color"] = "black"
    portrayal["r"] = 0.5
  elif type(agent) is Food:
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["Color"] = "green"
    portrayal["r"] = 0.35

  return portrayal

canvas = CanvasGrid(agent_portrayal, GRID_SIZE, GRID_SIZE, 500, 500)
server = mesa.visualization.ModularServer(AntFarmModel, [canvas], "Ant Farm Model")
server.port = 8521
server.launch()