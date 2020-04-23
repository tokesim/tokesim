#!/usr/bin/env python3
from tokesim.commands import commandline


def main() -> None:
    parser = commandline.setup_command_parsers()
    commandline.parse_commands(parser)


main()
