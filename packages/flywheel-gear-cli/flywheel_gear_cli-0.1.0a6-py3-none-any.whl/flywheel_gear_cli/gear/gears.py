"""Add gear commands to main parser."""
from . import gear_build, gear_config, gear_run, gear_update_env  # , gear_upload


def add_commands(subparsers, parsers, parents):  # pragma: no cover
    """Add gears commands to parser."""
    gear_parser = subparsers.add_parser("gear", help="Gear commands")
    parsers["gear"] = gear_parser

    gear_subparsers = gear_parser.add_subparsers(title="Available gear commands")

    gear_build_p = gear_build.add_command(gear_subparsers, parents)
    parsers["gear build"] = gear_build_p

    gear_update_env_p = gear_update_env.add_command(gear_subparsers, parents)
    parsers["gear update-env"] = gear_update_env_p
    gear_run_p = gear_run.add_command(gear_subparsers, parents)
    parsers["gear run"] = gear_run_p
    # gear_upload_p = gear_upload.add_command(gear_subparsers, parents)
    # parsers["gear upload"] = gear_upload_p

    gear_config_p = gear_config.add_command(gear_subparsers, parents)
    parsers["gear config"] = gear_config_p

    return gear_parser, gear_subparsers
