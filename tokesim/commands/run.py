import argparse

from tokesim.config import config_parser
from tokesim.simulation.sim import run_simulation


def parser_init_command(
    parent_parser: argparse.ArgumentParser, subparser: argparse._SubParsersAction
) -> None:
    run_parser = subparser.add_parser(
        "run",
        parents=[parent_parser],
        add_help=False,
        description="Launch a simulation",
        help="launches a simulation using tokesim",
    )
    run_parser.add_argument(
        "--config",
        dest="config",
        type=config_parser.parse_config,
        required=True,
        help="Simulation config file path",
    )
    run_parser.add_argument(
        "--port",
        dest="port",
        type=int,
        required=True,
        help="Sets port for the simulator",
    )

    run_parser.set_defaults(func=run_simulation)
