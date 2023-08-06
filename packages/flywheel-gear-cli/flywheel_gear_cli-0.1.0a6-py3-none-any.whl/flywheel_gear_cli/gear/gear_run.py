"""Gear run module."""
import argparse
import json
import logging
import os
import pty
import shutil
import subprocess
import sys
from pathlib import Path

from flywheel_gear_toolkit.utils.config import Config, ConfigValidationError

from ..utils import adjust_run_sh, get_docker_command, validate_manifest

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add run module."""
    parser = subparsers.add_parser(
        "run",
        parents=parents,
        help="Mimic a flywheel gear run locally.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Flywheel gears run with the following directory structure.

        /flywheel/v0
        ├── config.json
        ├── manifest.json
        ├── input
        │   ├── ...
        │   └── input1.nii.gz
        ├── output
        └── work

        Therefore to mimic a flywheel gear structure, this should be present
        locally and mounted into the container that runs the gear.

        If this structure is already present, either built manually, or from
        `fw job pull`, youi can run `fw gear run` directly from this directory.

        If this structure is NOT already present, `fw gear run` will prepare
        this structure in a target directory if you specify the
        `--target <dir>` flag.
        """,
    )
    parser.add_argument(
        "dir",
        nargs="?",
        help="""
            Location of the gear directory (optional, default=$PWD)

            Directory must contain at minimum manifest to determine
            docker image to use. Must also contain a config.json if
            the --target flag is specified.
            """,
    )
    parser.add_argument(
        "--target",
        help=(
            "Location where to prepare gear run directory (optional,"
            "default=/tmp/gear/<gear_name>_<gear_version>)"
        ),
    )
    parser.add_argument(
        "--no-rm",
        action="store_true",
        help="Don't remove container after run has finished",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactively",
    )
    parser.add_argument(
        "--mount-cwd",
        action="store_true",
        help="Mount entire Current Working Directory",
    )
    parser.add_argument("-e", "--entrypoint", help="Override container entrypoint")
    parser.add_argument(
        "-v",
        "--volumes",
        nargs="*",
        help="""
      List of volumes to attach in docker format, i.e.

      -v "~/config:/flywheel/v0/input" "~/output:/flywheel/v0/output"

      """,
    )

    parser.set_defaults(func=gear_run)
    parser.set_defaults(parser=parser)
    return parser


def gear_run(args):
    """Main gear run entrypoint."""
    # https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python
    # ^ need this for interactivity
    target = getattr(args, "target", None)
    assets = getattr(args, "dir", None) or Path.cwd()
    volumes = getattr(args, "volumes", None) or []
    asset_dir = Path(assets).resolve()
    if target:
        log.info("Creating directories")
        try:
            image, target_dir = setup(
                getattr(args, "dir", Path.cwd()),
                target=getattr(args, "target", None),
            )
        except ValueError:
            log.error("Setup failed.")
            return 1
        cmdline = get_docker_command(
            target_dir,
            volumes=[vol.split(":") for vol in volumes],
            mount_cwd=args.mount_cwd,
            no_rm=args.no_rm,
            interactive=args.interactive,
            entrypoint=getattr(args, "entrypoint", None),
        )
        run_script = target_dir / "run.sh"
        log.info("Writing run.sh script")
        with open(run_script, "w") as fp:
            fp.write("#! /bin/bash \n\n")
            fp.write(f"IMAGE={image}\n\n")
            fp.write("# Command:\n")
            fp.write(cmdline)
            fp.write("\n")
        log.info(cmdline)
        asset_dir = target_dir

    if not (asset_dir.exists() and asset_dir.is_dir()):
        log.error(f"Cannot find asset directory {asset_dir.resolve()}")
        return 1
    run_script = asset_dir / "run.sh"
    if not run_script.exists():
        log.error(
            "Could not find run.sh script. "
            f"Is this the right directory? ({asset_dir})"
        )
        return 1
    log.info("Running run.sh from assets directory...")
    if not target:
        # Don't need to do this if target was passed
        adjust_run_sh(
            run_script,
            volumes=[vol.split(":") for vol in volumes],
            mount_cwd=args.mount_cwd,
            no_rm=args.no_rm,
            interactive=args.interactive,
            entrypoint=getattr(args, "entrypoint", None),
        )
    os.chmod(str(run_script), 0o0755)
    if args.interactive:
        # handle_interactive_run(run_script)
        pty.spawn([str(run_script)])
    else:
        try:
            subprocess.check_output([str(run_script)])
        except subprocess.CalledProcessError as e:
            return e.returncode
    return 0


# def handle_interactive_run(run_script):  # pragma: no cover
#    # https://stackoverflow.com/a/43012138
#
#    # save original tty setting then set it to raw mode
#    old_tty = termios.tcgetattr(sys.stdin)
#    tty.setraw(sys.stdin.fileno())
#
#    # open pseudo-terminal to interact with subprocess
#    primary_fd, secondary_fd = pty.openpty()
#    try:
#        # Open a process with in/out/error going to secondary_fd
#        p = subprocess.Popen(
#            [str(run_script)],
#            stdin=secondary_fd,
#            stdout=secondary_fd,
#            stderr=secondary_fd,
#            universal_newlines=True,
#        )
#
#        while p.poll() is None:
#            # Wait until either stdin or primary_fd are available for reading.
#            readable, _, _ = select.select([sys.stdin, primary_fd], [], [])
#            if sys.stdin in readable:
#                # Write from stdin to pty
#                d = os.read(sys.stdin.fileno(), 10240)
#                os.write(primary_fd, d)
#            elif primary_fd in readable:
#                # Write from pty to stdout
#                o = os.read(primary_fd, 10240)
#                if o:
#                    os.write(sys.stdout.fileno(), o)
#    finally:
#        # restore tty settings back
#        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


def setup(wdir, target=None):  # pylint: disable=too-many-locals
    """Perform setup actions."""
    log.debug("Setting up")
    workdir = Path(wdir).resolve()
    ############# Config validation
    config = _validate_config(workdir)

    ############# Manifest validation
    manifest = validate_manifest(workdir / "manifest.json")

    # Populate directory structure
    if not target:
        target_dir = Path(f"/tmp/gear/{manifest.name}_{manifest.version}")
    else:
        target_dir = Path(target)
    target_dir.mkdir(parents=True, exist_ok=True)
    for path in ["input", "output", "work"]:
        new_dir = target_dir / path
        new_dir.mkdir(exist_ok=True)

    input_map = {}
    input_map_f = Path("~/.cache/flywheel/input_map.json").expanduser()
    try:
        with open(input_map_f, "r") as fp:
            input_map = json.load(fp)
    except FileNotFoundError:
        pass
    for key, val in manifest.inputs.items():
        if val["base"] == "file" and key in config.inputs:
            input_item = target_dir / f"input/{key}"
            input_item.mkdir(exist_ok=True)
            conf_val = config.inputs[key]
            docker_input = Path(conf_val["location"]["path"])
            if str(docker_input) in input_map.keys():
                local_path = input_map[str(docker_input)]
                target = target_dir / f"input/{key}/{docker_input.name}"
                log.info(
                    f"Found file input with local path: {local_path}, "
                    f"copying to target: {target}"
                )
                try:
                    shutil.copy(str(local_path), str(target))
                except:  # pylint: disable=bare-except
                    log.error(
                        "Couldn't copy input "
                        f"{local_path}"
                        " please ensure it exists."
                    )
            else:
                log.warning(
                    "Local path for input {key} not found. "
                    "Try adding with `fw gear config --{key} <path>"
                )
    try:
        shutil.copy(str(workdir / "config.json"), str(target_dir / "config.json"))
        shutil.copy(str(workdir / "manifest.json"), str(target_dir / "manifest.json"))
    except shutil.SameFileError:
        pass
    return manifest.get_docker_image_name_tag(), target_dir


def _validate_config(workdir):
    """Validate config.json, return config object if successful fail otherwise.

    Args:
        workdir (str): dir argument from argparser

    Returns:
        Config: config object from flywheel_gear_toolkit.utils.config
    """
    config_path = Path(workdir) / "config.json"

    if not config_path.is_file():
        log.error(
            """
            A config must be present to run a gear

            If you want to create a config for your gear, please run
            `fw gear config`
            """
        )
        sys.exit(1)
    try:
        conf = Config(path=config_path)
    except ConfigValidationError as err:
        log.error(err)
        sys.exit(1)

    return conf
