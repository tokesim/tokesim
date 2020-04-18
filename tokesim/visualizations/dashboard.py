from abc import ABC, abstractclassmethod
from typing import Any, Sequence

from mesa.visualization.ModularVisualization import VisualizationElement


# agent type


class Dashboard(ABC):
    @abstractclassmethod
    def get_elements(cls, model_params: Any) -> Sequence[VisualizationElement]:
        pass
