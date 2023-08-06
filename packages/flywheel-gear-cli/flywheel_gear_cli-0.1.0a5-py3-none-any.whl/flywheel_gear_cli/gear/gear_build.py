"""Gear build module."""
import logging
import sys
from pathlib import Path

import docker
from flywheel_gear_toolkit.utils.manifest import Manifest, ManifestValidationError

from ..utils import handle_docker_build

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def add_command(subparsers, parents):
    """Add gear build module."""
    parser = subparsers.add_parser(
        "build", parents=parents, help="Build docker image for gear"
    )
    parser.add_argument(
        "dir", nargs="?", help="Directory to mount (optional, default=$PWD)"
    )
    parser.add_argument(
        "--no-rm",
        action="store_true",
        help="Don't remove intermediate containers",
    )
    parser.add_argument(
        "--no-pull",
        action="store_true",
        help="Don't download updates for FROM in Dockerfile",
    )
    parser.add_argument(
        "--build-args",
        nargs="*",
        help='<key>=<value> list of build arguments to pass to the container, \
                ex. "--build-args image=test:0.1 cmd=/bin/bash"',
    )

    parser.set_defaults(func=gear_build)
    parser.set_defaults(parser=parser)
    return parser


def gear_build(args):
    """Build docker container.

    Args:
        args: Populated namespace from argparse

    """
    # Validate args

    image_tag, mount_dir, build_args = validate_args(args)

    # Build image
    log.info("Building docker image")
    im_id = handle_docker(
        image_tag,
        mount_dir,
        build_args,
        pull=(not getattr(args, "no_pull", False)),
        rm=(not getattr(args, "no_rm", False)),
    )
    log.info(f"Build image with id: {im_id}")
    return 0


def handle_docker(image_tag, mount_dir, build_args, pull=True, rm=True):
    """Handle docker image building."""
    # May not work on windows, see
    # https://github.com/docker/for-win/issues/4642
    client = docker.APIClient(base_url="unix://var/run/docker.sock")

    # If we are here, we have a Dockerfile, manifest, and run.py.  So build the image
    log.info(f"{'-'*20}Docker output{'-'*20}")
    stream = client.build(
        path=str(mount_dir.resolve()),
        tag=image_tag,
        rm=rm,
        pull=pull,
        buildargs=build_args,
        decode=True,
    )
    image_id = handle_docker_build(stream)

    log.info(f"{'-'*20}End docker output{'-'*20}")
    return image_id


def validate_args(args):
    """Helper function to validate arguments."""
    mount_dir = Path(args.dir) if getattr(args, "dir", False) else Path.cwd()
    manifest_file = mount_dir / "manifest.json"
    docker_file = mount_dir / "Dockerfile"
    run_file = mount_dir / "run.py"

    # Mount dir must be directory and exist
    if not mount_dir.is_dir():
        log.error(f"{str(mount_dir.resolve())} is not a valid path.  Exiting.")
        sys.exit(1)

    # Dockerfile must exists=
    if not docker_file.exists():
        log.error(
            f"{docker_file.resolve()} does not exist."
            f" Please make sure there is a Dockerfile in {mount_dir.resolve()}"
        )
        sys.exit(1)

    # Warn if run.py doesn't exist
    if not run_file.exists():
        log.warning(
            f"{run_file.resolve()} does not exist."
            " Docker container will not run correctly."
        )

    try:
        manifest = Manifest(str(manifest_file.resolve()))
        manifest.validate()
        image_tag = manifest.get_docker_image_name_tag()
    except FileNotFoundError as e:
        log.error(e)
        sys.exit(1)
    except ManifestValidationError as e:
        log.error(e)
        sys.exit(1)

    # TODO: needs to be tested
    build_arg_list = getattr(args, "build_args", [])
    build_args = {}
    if build_arg_list:
        for arg in build_arg_list:
            key, val = arg.split("=")
            build_args[key] = val

    return image_tag, mount_dir, build_args
