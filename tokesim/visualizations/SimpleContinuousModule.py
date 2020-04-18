import os
from typing import Any, Callable, NamedTuple

from mesa.visualization.ModularVisualization import VisualizationElement


class Position(NamedTuple):
    x: float
    y: float


SimpleSpace = Callable[[Any, Any], Position]
# TODO a strongly type
SpaceRender = Callable[[Any, Any, Any], SimpleSpace]
# TODO should return a more strongly typed response
AgentRender = Callable[[Any], Any]


class SimpleCanvas(VisualizationElement):
    local_includes = [f"{os.path.dirname(__file__)}/simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(
        self,
        portrayal_method: AgentRender,
        space: SpaceRender,
        canvas_height: int = 500,
        canvas_width: int = 500,
    ) -> None:
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        self.js_code = "elements.push(" + new_element + ");"
        self.space_render = space

    def render(self, model: Any) -> Any:
        space_state = []
        space = self.space_render(model, self.canvas_height, self.canvas_width)
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)  # type: ignore
            pos = space(portrayal["x"], portrayal["y"])
            portrayal["x"] = pos.x
            portrayal["y"] = pos.y
            space_state.append(portrayal)
        return space_state
