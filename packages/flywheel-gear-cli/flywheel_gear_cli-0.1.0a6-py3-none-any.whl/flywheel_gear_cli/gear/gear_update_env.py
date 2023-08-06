"""Gear update env command."""
import json
import logging
import sys
from pathlib import Path

import docker
from flywheel_gear_toolkit.utils.manifest import Manifest, ManifestValidationError

log = logging.getLogger(__name__)


# TODO: Add to blocklist?
BLOCKLIST = {"TERM", "HOSTNAME", "HOME"}


def add_command(subparsers, parents):
    """Add build module."""
    parser = subparsers.add_parser(
        "update-env",
        parents=parents,
        help="Update environment from docker container in manifest",
    )
    parser.add_argument(
        "dir", nargs="?", help="Directory to mount (optional, default=$PWD)"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Don't update env, only show what would be updated",
    )
    parser.add_argument(
        "-b",
        "--blocklist",
        nargs="*",
        help=f"""
        List of <key>=<value> environmental variables to add to or override default block list, where <value> is either 'yes' or 'no' ex. ... --blocklist TERM=yes LSCOLORS=no, this example would exclude TERM but include LSCOLORS in the environment added to the manifest.

        Default blocklist: {','.join(BLOCKLIST)}

        Note: If an environmental variable is already set in the manifest, and you
        add it to the blocklist, it will NOT be removed. The blocklist just specifies
        which values will not be updated.
        """,
    )
    parser.set_defaults(func=gear_update_env)
    parser.set_defaults(parser=parser)

    return parser


def gear_update_env(args):
    """Build docker container.

    Args:
        args: Populated namespace from argparse

    """
    manifest, manifest_file, blocklist, dry_run = validate_args(args)
    # Docker client
    log.debug("Init docker client")
    client = docker.from_env()

    env_gen = client.containers.run(
        image=manifest.get_docker_image_name_tag(),
        entrypoint="printenv",
        remove=True,
        stderr=False,
        stream=True,
    )

    handle_env(env_gen, manifest, manifest_file, blocklist, dry_run)


def validate_args(args):
    """Validate arguments."""
    blocklist = BLOCKLIST.copy()
    for block in getattr(args, "blocklist", []) or []:
        if "=" not in block:
            blocklist.add(block)
        else:
            key, val = str(block).split("=")
            if val == "yes":
                blocklist.add(key)
            elif val == "no":
                if key in blocklist:
                    blocklist.remove(key)
            else:
                log.error(
                    "Please enter blocklist in the format <key>=<value> where value"
                    " is either 'yes' or 'no' or just <key> to assume yes"
                )
                sys.exit(1)

    mount_dir = Path(args.dir) if getattr(args, "dir", None) else Path.cwd()

    if not mount_dir.is_dir():
        log.error(f"{str(mount_dir.resolve())} is not a valid path.  Exiting.")
        sys.exit(1)

    manifest_file = mount_dir / "manifest.json"

    try:
        manifest = Manifest(str(manifest_file.resolve()))
        manifest.validate()
    except FileNotFoundError as e:
        log.error(e)
        sys.exit(1)
    except ManifestValidationError as e:
        log.error(e)
        sys.exit(1)

    return (
        manifest,
        manifest_file,
        blocklist,
        getattr(args, "dry_run", False),
    )


def handle_env(env_gen, manifest, manifest_file, blocklist, dry_run):
    """Handle environment variables."""
    log.debug("Blocklist: %s", ", ".join(blocklist))
    docker_env = {}

    for env in env_gen:
        env = env.decode("utf-8").strip("\r\n")
        key, val, *_ = env.split("=")
        if key not in blocklist:
            docker_env[key] = val

    # If manifest already has some environment keys in it, keep those
    manifest.environment.update(docker_env)
    if dry_run:
        log.info(
            "Would write to manifest.json env: "
            f"{json.dumps(manifest.manifest.get('environment'), indent=2)}"
        )
    else:
        manifest.to_json(str(manifest_file.resolve()))
        log.info(
            "Successfully wrote environment to Manifest: "
            f"{json.dumps(manifest.manifest.get('environment'), indent=2)}"
        )
