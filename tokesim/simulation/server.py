from mesa.visualization.ModularVisualization import ModularServer

from tokesim.client.tokesim import TokesimClient
from tokesim.config.config_parser import ParsedConfig
from tokesim.models.ethereum_model import EthereumModelConfig
from tokesim.models.model import SimulationConfig


# replace this with something more general


def launch_server(
    config: ParsedConfig,
    rpcPort: str,
    chainId: int,
    simulationId: str,
    client: TokesimClient,
) -> None:

    model_spec = config.config_class_ref.get_spec(config.model_params)
    ethereum_config = EthereumModelConfig(
        config=config,
        model_spec=model_spec,
        rpcPort=rpcPort,
        chainId=chainId,
        simulationId=simulationId,
    )

    simulation_config = SimulationConfig(
        config=ethereum_config,
        width=100,
        height=100,
        simulationId=simulationId,
        client=client,
    )

    server = ModularServer(
        config.class_ref,
        config.dashboard_class_ref.get_elements(simulation_config),
        "Linear Bonded Token Model: Minority Majority Game",
        {
            "config": simulation_config.config,
            "width": simulation_config.width,
            "height": simulation_config.height,
            "simulationId": simulation_config.simulationId,
            "client": client,
        },
    )
    server.description = """
    This Example Token Contract models a linear token curve where the function mimiced directly tracks
    the token supply by a constant factor of 10000.  price = 10000 * x ; Where X = the total supply of tokens in the market.
    The agents are playing a mixed minority majority game. Where 40% follow the majority when known,
    and 60% follow the minority when known. These types of games have been used to simulate stock market pricing changes
    """

    server.launch()
