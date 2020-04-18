from typing import Any, Dict, Sequence, TypeVar

from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from tokesim.template.ethereum.simple_token_agent import SimpleTokenAgent
from tokesim.template.ethereum.simple_token_model import SimpleTokenModel
from tokesim.visualizations.SimpleContinuousModule import Position, SimpleSpace
from tokesim.visualizations.dashboard import Dashboard


S = TypeVar("S")
H = TypeVar("H")


def model_space(model: SimpleTokenModel, grid_h: int, grid_w: int) -> SimpleSpace:
    def space(current_budget: int, agent_no: int) -> Position:
        budget = model.initial_capital()
        x = (
            current_budget / budget
        )  # shows proportion of total wealth that's caputured by an agent
        y = float(agent_no) / len(model.agents)
        return Position(x=x, y=y)

    return space


def agent_draw(agent: SimpleTokenAgent[S, H]) -> Dict[str, Any]:
    x = agent.budget()
    y = agent.unique_id
    return {"Shape": "circle", "r": 5, "Filled": "true", "Color": "Red", "x": x, "y": y}


class SimpleTokenDashboard(Dashboard):
    @classmethod
    def get_elements(cls, model_params: Any) -> Sequence[VisualizationElement]:
        token_chart = ChartModule(
            [
                {"Label": "token_supply", "Color": "Black"},
                {"Label": "token_price", "Color": "Blue"},
            ],
            data_collector_name="datacollector",
        )
        # TODO agent needs more features in order to make budget view more useful
        # TODO models that implement simple canavas must implement space current untyped
        # budget_view = SimpleCanvas(agent_draw, model_space)
        return [token_chart]
