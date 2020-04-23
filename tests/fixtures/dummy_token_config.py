from typing import Any

from mesa.time import RandomActivation

from tokesim.models.ethereum_model import EthereumModelSpec, ModelSpec


class DummyTokenConfig(EthereumModelSpec[Any, Any]):
    def get_spec(params: Any) -> ModelSpec[Any, Any]:
        return ModelSpec(agent_population=[], schedule=RandomActivation, history=[],)
