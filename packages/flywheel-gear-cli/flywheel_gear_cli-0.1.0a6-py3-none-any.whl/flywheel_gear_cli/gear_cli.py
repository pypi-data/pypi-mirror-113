"""Main gear_cli entry."""
import argparse
import logging
import os
import sys

from .gear import gears
from .job import jobs
from .logging import configure_logging

log = logging.getLogger(__name__)


def set_subparser_print_help(parser, subparsers):  # pragma: no cover
    """Set subcommands help."""

    def print_subcommands_help(args):  # pylint: disable=unused-argument
        parser.print_help()

    parser.set_defaults(func=print_subcommands_help)

    help_parser = subparsers.add_parser("help", help="Print this help message and exit")
    help_parser.set_defaults(func=print_subcommands_help)


def get_config(args):  # pragma: no cover
    """Get config."""
    # configure logging
    if os.environ.get("FW_DISABLE_LOGS") != "1":
        configure_logging(args)


def get_global_parser():  # pragma: no cover
    """Get global parser."""
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Assume the answer is yes to all prompts",
    )

    log_title = parser.add_argument_group(title="Logging options")
    log_group = log_title.add_mutually_exclusive_group()
    log_group.add_argument("--debug", action="store_true", help="Turn on debug logging")
    log_group.add_argument(
        "--quiet",
        action="store_true",
        help="Squelch log messages to the console",
    )
    return parser


def print_help(default_parser, parsers):  # pragma: no cover
    """Print commands help."""

    def print_help_fn(args):
        subcommands = " ".join(args.subcommands)
        if subcommands in parsers:
            parsers[subcommands].print_help()
        else:
            default_parser.print_help()

    return print_help_fn


def add_commands(parser):  # pragma: no cover
    """Add commands to parser."""
    # global_parser = get_global_parser()
    parser.set_defaults(config=get_config)

    global_parser = get_global_parser()

    parsers = {}
    subparsers = parser.add_subparsers(title="Available commands", metavar="")

    gear_parser, gear_subparsers = gears.add_commands(
        subparsers, parsers, parents=[global_parser]
    )
    set_subparser_print_help(gear_parser, gear_subparsers)
    job_parser, job_subparsers = jobs.add_commands(
        subparsers, parsers, parents=[global_parser]
    )
    set_subparser_print_help(job_parser, job_subparsers)

    parser_help = subparsers.add_parser("help")
    parsers["help"] = parser_help
    parser_help.add_argument("subcommands", nargs="*")
    parser_help.set_defaults(func=print_help(parser, parsers))


def main():  # pragma: no cover
    """Main entry."""
    parser = argparse.ArgumentParser(
        prog="gear_cli", description="Flywheel gear cli interface"
    )

    add_commands(parser)

    args = parser.parse_args()
    # Additional configuration
    try:
        config_fn = getattr(args, "config", None)
        if callable(config_fn):
            config_fn(args)  # pylint: disable=not-callable
    except Exception as e:  # pylint: disable=broad-except
        log.error(e)
        sys.exit(1)

    func = getattr(args, "func", None)
    if func is not None:
        try:
            result = args.func(args)
            if result is None:
                result = 0
        except Exception:  # pylint: disable=broad-except
            log.error("Uncaught Exception", exc_info=True)
            result = 1

    else:
        parser.print_help()
        result = 1

    sys.exit(result)


if __name__ == "__main__":  # pragma: no cover

    main()
