"""General utils module."""
import functools
import json
import logging
import os
import re
import sys
import typing as t
from datetime import datetime
from pathlib import Path

import colorama
import flywheel
import humanize
from flywheel_gear_toolkit.utils.manifest import Manifest, ManifestValidationError
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

auth_config = Path("~/.config/flywheel/user.json").expanduser()


@functools.lru_cache(maxsize=10)
def get_sdk_client(api_key: str) -> flywheel.Client:
    """Helper to get and cache SDK client."""
    return flywheel.Client(api_key)


@functools.lru_cache(maxsize=10)
def load_auth_config():
    """Helper to get and cache auth config file."""
    try:
        with open(auth_config, "r") as f:
            config = json.load(f)
    except (IOError, json.decoder.JSONDecodeError):
        config = {}
    return config


def get_credentials(api_key):
    """Get information from API key.

    Args:
        api_key (str):  Flywheel api key

    Returns:
        api_key (dict): Dictionary of attributes
            * host: domain name of flywheel server
            * unique: unique portion
            * api_key: Full api_key
            * port: Port of server
            * opt: option, e.g. __force_insecure
    """
    resp = {}
    full = api_key.split(":")

    resp["unique"] = full[-1]
    resp["host"] = full[0]
    resp["api_key"] = f"{full[0]}:{full[-1]}"
    resp["port"] = None
    resp["opt"] = None

    port_match = r"^(\d{1,5})$"  # Match numeric 1-5 decimals
    opt_match = r"([^\s:]+)"  # Match anything but spaces and colons
    for section in full[1:-1]:
        port = re.match(port_match, section)
        opt = re.match(opt_match, section)
        if port:
            resp["port"] = port.group(1)
        if opt:
            resp["opt"] = opt.group(1)

    return resp


def adjust_run_sh(  # pylint: disable=too-many-arguments
    run_script: Path,
    volumes: t.Optional[t.List[str]] = None,
    mount_cwd: bool = False,
    no_rm: bool = False,
    interactive: bool = False,
    entrypoint: t.Optional[str] = None,
) -> None:
    """Helper function to adjust the run.sh script."""
    lines = []
    with open(run_script, "r") as fp:
        lines = fp.readlines()

    docker_cmd_start = 0
    for i, line in enumerate(lines):
        if "docker" in line:
            docker_cmd_start = i
            break

    lines = lines[:docker_cmd_start]
    new_cmd = get_docker_command(
        run_script.parents[0],
        volumes=volumes,
        mount_cwd=mount_cwd,
        no_rm=no_rm,
        interactive=interactive,
        entrypoint=entrypoint,
    )
    lines.append(new_cmd)
    with open(run_script, "w") as fp:
        for line in lines:
            fp.write(line)


def get_docker_command(  # pylint: disable=too-many-arguments
    root_dir,
    volumes=None,
    mount_cwd=False,
    no_rm=False,
    interactive=False,
    entrypoint=None,
) -> str:
    """Return docker command with mount volumes and image.

    Args:
        root_dir (Path-like): Path where to save the assets
        volumes (list): List of volumes to mount
        mount_cwd (bool): Where or not to mount the current working directory
        no_rm (bool): If True, don't remove container when done. Default False
        interactive (bool): If True, run the container interactively.
            Default False,
        entrypoint (str, None): If present, override the default entrypoint.

    Returns:
        (str): The docker command
    """
    cmdline = (
        "docker run "
        + ("" if no_rm else "--rm ")
        + ("-it " if interactive else "")
        + (f"--entrypoint={entrypoint} \\\n " if entrypoint else "\\\n")
    )
    dirs_to_mount = [
        (root_dir / "input", "/flywheel/v0/input"),
        (root_dir / "output", "/flywheel/v0/output"),
        (root_dir / "work", "/flywheel/v0/work"),
        (root_dir / "config.json", "/flywheel/v0/config.json"),
        (root_dir / "manifest.json", "/flywheel/v0/manifest.json"),
    ]

    if mount_cwd:
        dirs_to_mount = [(Path.cwd(), "/flywheel/v0")]
    if volumes:
        dirs_to_mount.extend(volumes)

    for (local, docker) in dirs_to_mount:
        if not local.exists():
            log.warning(f"{local} does not exist, skipping.")
            continue
        cmdline += f"\t-v {local}:{docker} \\\n"

    cmdline = cmdline + "\t$IMAGE"

    return cmdline


class Progress(BaseModel):
    """Model for progress bar."""

    current: t.Optional[int] = 0
    total: t.Optional[int] = 0
    start: t.Optional[int] = 0
    units: t.Optional[str] = ""
    width: int = 0

    def in_progress(self):
        """Return True if in progress, False otherwise."""
        return (
            self.total != 0 or self.current != 0 or self.start != 0 or self.units != ""
        )

    def __repr__(self):
        """String representation."""
        if self.current <= 0 and self.total <= 0:
            return ""
        if self.total <= 0:
            if self.units:
                return f"{self.current} {self.units}"
            return humanize.naturalsize(self.current)
        ratio = float(self.current) / float(self.total)
        ratio = min(ratio, 1)
        bar_width = int(self.width / 4)
        bar_chars = int(ratio * bar_width)
        bar_block = f"{'='*(bar_chars)}>{' '*(bar_width - bar_chars)}"
        text = ""
        if self.units:
            text = f"{self.current}/{self.total} {self.units}"
        else:
            curr = humanize.naturalsize(self.current)
            tot = humanize.naturalsize(self.total)
            text = f"{curr}/{tot}"

        left = 0
        if self.current > 0 and self.start > 0 and ratio < 1:
            time_passed = (
                datetime.now().timestamp()
                - datetime.fromtimestamp(self.start).timestamp()
            )
            rate = float(self.current) / float(time_passed)
            left = (self.total - self.current) * rate

        return f"{bar_block} {text} {left if left else ''}"


class DockerMessage(BaseModel):
    """Model for message from docker api."""

    stream: t.Optional[str] = None
    status: t.Optional[str] = None
    progress: t.Optional[Progress] = Field(alias="progressDetail", default=None)
    id: t.Optional[str] = None
    from_: t.Optional[str] = Field(alias="from", default=None)
    time: t.Optional[int] = None
    # errorDetail*JSONError
    error_message: t.Optional[str] = Field(alias="error", default=None)
    aux: t.Optional[dict]


def up(n):
    """Ascii control move cursor up."""
    return colorama.Cursor.UP(n) + "\r"


def down(n):
    """Ascii control move cursor down."""
    return colorama.Cursor.DOWN(n) + "\r"


def handle_docker_build(stream: t.Generator[dict, None, None]):
    """Handle generator of docker api messages."""
    layers: t.Dict[str, int] = dict()
    image_id = ""
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 100
    for line in stream:
        msg = DockerMessage(**line)
        diff = 0
        if msg.aux:
            if "ID" in msg.aux:
                sys.stdout.write(f"ID: {msg.aux['ID']}\n")
                image_id = msg.aux["ID"]
                continue
        if msg.id:
            if msg.progress:
                msg.progress.width = width
                if msg.id not in layers:
                    line_no = len(layers)
                    layers[msg.id] = line_no
                    sys.stdout.write("\n")
                diff = len(layers) - layers[msg.id]
                sys.stdout.write(up(diff))
                sys.stdout.write(colorama.ansi.clear_line())
            else:
                layers = dict()
        if msg.stream:
            layers = dict()
            sys.stdout.write(msg.stream)
            continue
        write_line(msg)
        if msg.id:
            sys.stdout.write(down(diff))

        sys.stdout.flush()
    return image_id


def handle_docker_push(stream: t.Generator[dict, None, None]):
    """Handle generator of docker api messages."""
    layers: t.Dict[str, int] = dict()
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 100
    for line in stream:
        msg = DockerMessage(**line)
        diff = 0
        if msg.aux:
            if "Digest" in msg.aux:
                sys.stdout.write("Digest: " + str(msg.aux["Digest"]))
                return msg.aux["Digest"]
        if msg.id:
            if msg.progress:
                msg.progress.width = width
                if msg.id not in layers:
                    line_no = len(layers)
                    layers[msg.id] = line_no
                    sys.stdout.write("\n")
                diff = len(layers) - layers[msg.id]
                sys.stdout.write(up(diff))
                sys.stdout.write(colorama.ansi.clear_line())
            else:
                layers = dict()
        write_line(msg)
        if msg.id:
            sys.stdout.write(down(diff))

        sys.stdout.flush()
    return None


def write_line(line):
    """Write line to console."""
    if line.progress and line.progress.in_progress():
        sys.stdout.write(f"{line.id}: {repr(line.progress)}")
    else:
        msg = f"{line.id}: " if line.id else ""
        msg += line.status
        msg += "\n"
        sys.stdout.write(msg)


def validate_manifest(manifest_path):
    """Validate manifest.json, return manifest object if successful, fail otherwise.

    Args:
        manifest_path (Path): Path to manifest.json

    Returns:
        Manifest: manifest object from flywheel_gear_toolkit.utils.manifest
    """
    if not manifest_path.is_file():
        log.error("A manifest is required to prepare gear run")
        sys.exit(1)
    try:
        manifest = Manifest(manifest=manifest_path)
        manifest.validate()
    except ManifestValidationError as e:
        log.error(e)
        sys.exit(1)

    return manifest
