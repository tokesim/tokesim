import argparse

from tokesim.commands import initialize, run


def setup_command_parsers() -> argparse.ArgumentParser:
    parent_parser = argparse.ArgumentParser(
        description="Launch Token Economics Simulator"
    )
    parent_parser.set_defaults(func=None)
    subparser = parent_parser.add_subparsers(title="actions")
    initialize.parser_init_command(parent_parser, subparser)
    run.parser_init_command(parent_parser, subparser)
    return parent_parser


def parse_commands(parent_parser: argparse.ArgumentParser):
    args = parent_parser.parse_args()
    if args.func is None:
        parent_parser.exit(1, "Could missing subcommand! (init or run) \n")
    args.func(args)
