from typing import NamedTuple, cast

from tokesim.client.generated_types import Accounts, Chain
from tokesim.client.tokesim import TokesimClient
from tokesim.config.config_parser import ParsedConfig
from tokesim.config.configuration import AccountsConfig
from tokesim.simulation import server


class SimulationLaunchParams(NamedTuple):
    config: ParsedConfig
    port: int


def generate_account_config_from_model(config: ParsedConfig) -> AccountsConfig:
    # TODO if a distribution method is defined for the model allow the model to define the
    # initial balance allocations for the agents using the balance_distribution method
    """
    if(type(config.class_ref.balance_distribution) is Callable):
       config.class_ref.balance_distribution()
    """
    return config.accounts


def run_simulation(params: SimulationLaunchParams) -> None:
    config: ParsedConfig = params.config
    client = TokesimClient(f"http://localhost:{params.port}")
    accounts = generate_account_config_from_model(config)
    result = client.start_simulation(
        {"chain": Chain("ethereum"), "accounts": cast(Accounts, accounts)}
    )
    simulationId = result["id"]
    rpcPort = result["meta"]["rpcPort"]
    chainId = result["meta"]["chainId"]
    server.launch_server(config, rpcPort, chainId, simulationId, client)
