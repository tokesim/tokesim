import random
from typing import Callable, NamedTuple, Sequence

from mesa.time import RandomActivation
from mesa_behaviors.agents.base_agent import BaseAgent
from mesa_behaviors.agents.population import (
    AgentLabels,
    AgentPopulationGenerator,
    AgentTypeMap,
    generate_population,
)
from mesa_behaviors.history.binary import BinaryHistory
from mesa_behaviors.models.base_model import BaseModel
from mesa_behaviors.strategies import binary_strategy
import mesa_behaviors.utility.binary as binary_util


class DummyAgentFeatures(NamedTuple):
    tokens: int


class DummyAgent(
    BaseAgent[binary_strategy.BinaryStrategies, BinaryHistory, DummyAgentFeatures]
):
    def __init__(
        self,
        strategies: binary_strategy.BinaryStrategies,
        utility: binary_util.BaseUtility,
        historical_func: Callable[[], BinaryHistory],
        label: str,
    ) -> None:
        super().__init__(strategies, utility, historical_func, label)
        self.latest_scores: binary_util.BinaryUtilityScore = {}
        self.feature = DummyAgentFeatures(tokens=0)

    def features(self) -> DummyAgentFeatures:
        return self.feature

    def select(self, scores: binary_util.BinaryUtilityScore) -> int:
        score = sorted(scores.items(), key=lambda x: x[1]["score"])[-1][1]
        return score["prediction"]

    def step(self) -> None:

        self.latest_scores = self.utility.utility_score(self.strategies, self.history)
        action = self.select(self.latest_scores)
        if action == 1:
            self.feature = DummyAgentFeatures(tokens=1)
        else:
            self.feature = DummyAgentFeatures(tokens=0)

    def label(self) -> str:
        return self.label_name


class DummyModel(BaseModel):
    def __init__(
        self,
        agent_population: Sequence[BaseAgent],
        schedule: RandomActivation,
        history: BinaryHistory,
    ) -> None:
        super().__init__(agent_population, schedule, history)

    @classmethod
    def distro(cls) -> int:
        return 99


def dummy_distribution(agent_labels: AgentLabels, size: int) -> AgentLabels:
    return random.choices(agent_labels, k=size)


def population_generator(
    history: BinaryHistory, size: int
) -> AgentPopulationGenerator[int]:
    agentMap: AgentTypeMap[int] = {
        "minority": lambda: DummyAgent(
            binary_strategy.generate_binary_strategies(4, 3),
            binary_util.BinaryMinorityUtility(),
            history.retrieve,
            "minority",
        ),
        "majority": lambda: DummyAgent(
            binary_strategy.generate_binary_strategies(4, 3),
            binary_util.BinaryMajorityUtility(),
            history.retrieve,
            "majority",
        ),
    }
    return generate_population(dummy_distribution, agentMap, size)
