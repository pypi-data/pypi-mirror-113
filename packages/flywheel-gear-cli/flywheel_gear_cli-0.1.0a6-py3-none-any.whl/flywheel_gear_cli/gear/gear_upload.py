"""Gear Upload module."""
import json
import logging
import os
import sys
from pathlib import Path

import docker
from flywheel.rest import ApiException
from flywheel_gear_toolkit.utils.manifest import Manifest, ManifestValidationError

from ..utils import get_sdk_client, handle_docker_push

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add gears upload command."""
    parser = subparsers.add_parser(
        "upload",
        parents=parents,
        help="Upload gear from current working directory",
    )
    parser.add_argument(
        "dir",
        nargs="?",
        help="Directory of docker build context (optional, default=$PWD)",
    )
    parser.add_argument(
        "--keys", nargs="*", help="Flywheel API key(s) (space separated)"
    )

    parser.set_defaults(func=gear_upload)
    parser.set_defaults(parser=parser)

    return parser


def gear_upload(args):  # pylint: disable=too-many-locals
    """Upload current directory gear.

    Docker build, tag and push to Flywheel intance registry with configuration
    extracted from manifest.json, register gear to Flywheel instance.
    """
    if getattr(args, "keys", None):
        keys = args.keys
    else:  # use current credentials
        config_path = Path("~/.config/flywheel/user.json").expanduser()
        config = {}
        with open(config_path, "r") as fp:
            config = json.load(fp)
        keys = [config.get("key", "")]
    if getattr(args, "dir", None):
        manifest_path = Path(args.dir) / "manifest.json"
    else:
        manifest_path = Path.cwd() / "manifest.json"
    try:
        manifest = Manifest(manifest_path)
        manifest.validate()
    except ManifestValidationError as e:
        log.error(e)
        sys.exit(1)

    # GearDoc
    gear_doc = {
        "category": manifest.get_value("custom.gear-builder.category"),
        "gear": dict(manifest.manifest),
    }

    # gear-doc.custom.gear-builder.image
    src_image = manifest.get_docker_image_name_tag()
    try:
        for api_key in keys:

            fw = get_sdk_client(api_key)
            user = fw.get_current_user()
            domain = get_domain(api_key)

            log.info(f"Logging into docker registry {domain} as user {user.email}")
            docker_client = login(api_key, user, domain)

            add_gear(docker_client, src_image, gear_doc, fw, domain)
    except ValueError:
        return 1
    return 0


def add_gear(docker_client, src_image, gear_doc, fw, domain):
    """Handle adding gear to server.

    1. Prepare gear doc
    2. Call `fw.prepare_add_gear()` to get ticket to push to docker repo.
    3. Push image to registry and write output to console
    4. Confirm gear uploaded via `fw.save_gear()`
    """
    manifest = gear_doc["gear"]
    gear_name, gear_version = os.path.basename(src_image).split(":")
    # Tag image
    dst_gear = f"{domain}/{gear_name}"
    log.info(f"Tagging image locally as {dst_gear}:{gear_version}")
    image = docker_client.images.get(src_image)
    image.tag(dst_gear, gear_version)
    gear_doc.update(
        {
            "exchange": {
                "rootfs-url": f"docker://{dst_gear}:{gear_version}",
                "rootfs-hash": image.id,
            }
        }
    )
    # Get permission to push
    log.info("Getting permission to push image...")
    ticket = fw.prepare_add_gear(gear=gear_doc)
    # Push image
    log.info(f"Uploading {dst_gear}:{gear_version} to Docker registry...")
    try:
        stream = docker_client.images.push(
            dst_gear, tag=gear_version, stream=True, decode=True
        )
        digest = handle_docker_push(stream)
    except docker.errors.APIError as e:
        log.error("Error pushing image", exc_info=True)

    # Register gear
    log.info(f"Registering {dst_gear}:{gear_version} on server...")
    try:
        fw.save_gear({"ticket": ticket, "repo": manifest["name"], "pointer": digest})
        log.info(
            "Done! You should now see your gear in the Flywheel web interface or find"
            "it with `fw job list-gears`"
        )
    except ApiException as e:
        if e.status == 409:
            log.error("Gear already exists")
        else:
            log.error("Error occured uploading gear", exc_info=True)


def get_domain(api_key):
    """Helper function to get domain from api_key."""
    return api_key.split(":")[0]


def login(api_key, user, domain):
    """Log into docker registry."""
    # docker
    # log.info("Logging to Docker registry at %s...", domain)
    docker_client = docker.from_env()
    # - login
    registry = f"https://{domain}/v2"
    split_key = api_key.split(":")
    cleaned_key = ":".join([split_key[0], split_key[-1]])
    docker_client.login(username=user.email, password=cleaned_key, registry=registry)
    return docker_client
