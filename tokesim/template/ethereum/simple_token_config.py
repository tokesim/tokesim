import random
from typing import Any

from bitarray import bitarray
from mesa.time import RandomActivation
from mesa_behaviors.agents.population import (
    AgentLabels,
    AgentPopulationGenerator,
    AgentTypeMap,
    generate_population,
)
from mesa_behaviors.history.binary import BinaryHistory
from mesa_behaviors.strategies.binary_strategy import generate_binary_strategies
from mesa_behaviors.utility.binary import BinaryMajorityUtility, BinaryMinorityUtility

from tokesim.models.ethereum_model import EthereumModelSpec, ModelSpec
from tokesim.template.ethereum.simple_token_agent import (
    SimpleTokenAgent,
    SimpleTokenAgentFeatures,
)


def agent_generators(
    history: BinaryHistory, num_strategies: int, memory: int
) -> AgentTypeMap:
    return {
        "minority": lambda: SimpleTokenAgent(
            generate_binary_strategies(num_strategies, memory),
            BinaryMinorityUtility(),
            history.retrieve,
            "minority",
        ),
        "majority": lambda: SimpleTokenAgent(
            generate_binary_strategies(num_strategies, memory),
            BinaryMajorityUtility(),
            history.retrieve,
            "majority",
        ),
    }


SimpleTokenMixedGameSpec = ModelSpec[SimpleTokenAgentFeatures, BinaryHistory]


def uniform_mixed_game_distribution(
    agent_labels: AgentLabels, size: int
) -> AgentLabels:
    return random.choices(agent_labels, [0.60, 0.40], k=size)


def population_generator(
    agents: AgentTypeMap, num_agents: int
) -> AgentPopulationGenerator:
    return generate_population(uniform_mixed_game_distribution, agents, num_agents)


class SimpleTokenMixedGameRandom(
    EthereumModelSpec[SimpleTokenAgentFeatures, BinaryHistory]
):
    def get_spec(params: Any) -> SimpleTokenMixedGameSpec:

        memory = params["memory"]
        num_strategies = params["num_strategies"]

        initial_history = random.choices([1, 0], k=memory)
        history = BinaryHistory(bitarray(initial_history))
        agent_types = agent_generators(history, num_strategies, memory)

        return SimpleTokenMixedGameSpec(
            agent_population=population_generator(agent_types, params["num_agents"])(),
            schedule=RandomActivation,
            history=history,
        )
