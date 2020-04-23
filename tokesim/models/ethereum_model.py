from abc import ABC, abstractmethod
import dataclasses
from typing import Any, Generic, TypeVar

from mesa.time import BaseScheduler
from mesa_behaviors.agents.population import AgentPopulation
from mesa_behaviors.models.base_model import BaseModel

from tokesim.client.generated_types import SimulationId
from tokesim.client.tokesim import TokesimClient
from tokesim.config.config_parser import ParsedConfig


# Model FeatureSet
F = TypeVar("F")
# Model History format
H = TypeVar("H")
# Individual history item format
S = TypeVar("S")


@dataclasses.dataclass
class ModelSpec(Generic[F, H]):
    agent_population: AgentPopulation[F]
    schedule: BaseScheduler
    history: H


@dataclasses.dataclass
class EthereumModelConfig(Generic[F, H]):
    model_spec: ModelSpec[F, H]
    config: ParsedConfig
    rpcPort: str
    chainId: int
    simulationId: str


class EthereumModelSpec(ABC, Generic[F, H]):
    def get_spec(params: Any) -> ModelSpec[F, H]:
        pass


class EthereumModel(BaseModel, Generic[F, H], ABC):
    def __init__(self, config: EthereumModelConfig[F, H], client: TokesimClient):
        self.config = config
        self.client = client
        super().__init__(
            config.model_spec.agent_population,
            config.model_spec.schedule(self),
            config.model_spec.history,
        )
        self.deploy()

    def step(self) -> None:
        # start mining clear pending transactions
        self.client.start_block_transactions(SimulationId(self.config.simulationId))
        # stop mining
        self.client.end_block_transactions(SimulationId(self.config.simulationId))

    @abstractmethod
    def deploy(self) -> None:
        pass

    @abstractmethod
    def assign_accounts(self) -> None:
        pass

    @abstractmethod
    def assign_contracts(self) -> None:
        pass
