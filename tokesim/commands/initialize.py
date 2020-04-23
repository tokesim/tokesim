import argparse
from typing import Any

from tokesim.template.generator import generate_initial_template


def _init_simulation(args: Any) -> None:
    print(f"creating simulation template with ${args.dir} for ${args.agents}")
    generate_initial_template(args.dir, args.agents)
    exit(0)


def parser_init_command(
    parent_parser: argparse.ArgumentParser, subparser: argparse._SubParsersAction
) -> None:
    init_parser = subparser.add_parser(
        "init",
        parents=[parent_parser],
        add_help=False,
        description="Initialize new simulation",
        help="creates an initial simulation context",
    )
    init_parser.add_argument(
        "--dir", dest="dir", required=True, help="Simulation directory"
    )
    init_parser.add_argument(
        "--agents",
        dest="agents",
        type=int,
        help="Number of agents for the simulation",
        default=100,
    )
    init_parser.set_defaults(func=_init_simulation)
