"""Gear Validate Manifest module."""
import logging
from pathlib import Path

from flywheel_gear_cli.utils import validate_manifest

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add gears upload command."""
    parser = subparsers.add_parser(
        "validate-manifest",
        parents=parents,
        help="Validate gear manifest in current working directory or at path if "
        "provided",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="""
            Location of the manifest.json directory (optional, 
            default=$PWD/manifest.json)
            """,
    )
    parser.set_defaults(func=validate_manifest_wrapper)
    parser.set_defaults(parser=parser)

    return parser


def validate_manifest_wrapper(args):
    """Validate manifest in current working directory."""
    if getattr(args, "path", None):
        manifest_path = Path(args.path)
    else:
        manifest_path = Path.cwd() / "manifest.json"
    validate_manifest(manifest_path)
