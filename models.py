from typing import Any
import mesa
from agents import Ant, Food
from mesa.visualization.modules import CanvasGrid

GRID_SIZE = 25

class AntFarmModel(mesa.Model):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)

    self.grid = mesa.space.MultiGrid(GRID_SIZE, GRID_SIZE, torus=True)
    self.schedule = mesa.time.SimultaneousActivation(self)

    for i in range(10):
      ant = Ant(i, self)
      x = self.random.randrange(self.grid.width)
      y = self.random.randrange(self.grid.height)
      self.grid.place_agent(ant, (x, y))
      self.schedule.add(ant)

    for _ in range(10):
      self._spawn_food_at_random_location()

  def _spawn_food_at_random_location(self) -> None:
    food = Food(self._last_agent_id() + 1, self)
    x = self.random.randrange(self.grid.width)
    y = self.random.randrange(self.grid.height)
    self.grid.place_agent(food, (x, y))
    self.schedule.add(food)

  def _last_agent_id(self) -> int:
    return max(self.schedule._agents.keys())

  def step(self) -> None:
    self.schedule.step()

def agent_portrayal(agent: mesa.Agent) -> dict:
  if agent is None:
    return
  
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
    portrayal["r"] = 0.5

  return portrayal

canvas = CanvasGrid(agent_portrayal, GRID_SIZE, GRID_SIZE, 500, 500)
server = mesa.visualization.ModularServer(AntFarmModel, [canvas], "Ant Farm Model")
server.port = 8521
server.launch()