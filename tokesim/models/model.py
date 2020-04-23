import dataclasses
from typing import Generic, TypeVar, Union

from tokesim.client.tokesim import TokesimClient
from tokesim.models.ethereum_model import EthereumModelConfig


F = TypeVar("F")
H = TypeVar("H")

ModelConfig = Union[EthereumModelConfig[F, H]]


@dataclasses.dataclass
class SimulationConfig(Generic[F, H]):
    config: ModelConfig[F, H]
    height: int
    width: int
    simulationId: str
    client: TokesimClient
