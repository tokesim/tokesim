from typing import Any, Sequence

from mesa.visualization.ModularVisualization import VisualizationElement

from tokesim.visualizations.dashboard import Dashboard


class DummyDashboard(Dashboard):
    @classmethod
    def get_elements(cls, model_params: Any) -> Sequence[VisualizationElement]:
        return []
