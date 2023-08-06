"""Job Pull module."""
import json
import logging
import os
from pathlib import Path

import flywheel

from ..utils import get_docker_command, load_auth_config

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add job pull command."""
    parser = subparsers.add_parser(
        "pull",
        parents=parents,
        help="Pull job assets and generate docker command to run job locally",
    )
    parser.add_argument("job_id", help="Job ID")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Output directory path (optional, default=$PWD)",
    )
    parser.add_argument(
        "-a",
        "--add-key",
        action="store_true",
        help="Replace api-key in config.json with current user one",
    )
    parser.add_argument(
        "-m",
        "--mnt-cwd",
        action="store_true",
        help="Mount current working directory to /flywheel/v0 in the generated docker "
        "command",
    )

    parser.set_defaults(func=job_pull)
    parser.set_defaults(parser=parser)

    return parser


def job_pull(args):
    """Pull job assets.

    Args:
        args: A populated namespace
    """
    # process args
    output_dir = args.output_dir if args.output_dir else os.getcwd()
    add_key = args.add_key

    fw = flywheel.Client()
    if not fw.get_current_user().root:
        raise ValueError("This process requires site-admin privileges!")

    log.info("Pulling assets for job %s", args.job_id)
    # Get the job
    job = fw.get_job(args.job_id)

    # Build the output directories
    root_dir = get_root_dir(job, output_dir)
    build_dirs(root_dir)

    # Pull job assets
    api_key = None
    if add_key:
        config = load_auth_config()
        api_key = config.get("key")
    ret = pull_job_assets(fw, job, root_dir, api_key)
    if ret:
        return 1

    # Generate run script
    gear = fw.get_gear(job.gear_id).gear
    image = gear.get("custom", {}).get("gear-builder").get("image")
    if not image:
        image = gear.get("custom", {}).get("docker-image")
    cmdline = get_docker_command(root_dir, mount_cwd=args.mnt_cwd)

    # Save cmdline as script
    run_script = root_dir / "run.sh"
    with open(run_script, "w") as fp:
        fp.write("#! /bin/bash \n\n")
        fp.write(f"IMAGE={image}\n\n")
        fp.write("# Command:\n")
        fp.write(cmdline)
        fp.write("\n")
    log.info(cmdline.replace("$IMAGE", image))
    log.info("Note: image name is stored in variable $IMAGE in run script.")
    return 0


def get_root_dir(job, output_dir):
    """Return folder path where to save jobs assets.

    Args:
        job (flywheel.Job): A Flywheel job object
        output_dir (Path-like): Root path where to save job assets

    Return:
        (Path-like): Path
    """
    return (
        Path(output_dir).expanduser().absolute()
        / f"{job.gear_info.name}-{job.gear_info.version}-{job.id}"
    )


def build_dirs(root_dir):
    """Build Flywheel directory structure at root_dir.

    Create `input` and `output` directory at `root_dir` path.

    Args:
        root_dir (Path-like): Path to a directory
    """
    input_dir = root_dir / "input"
    output_dir = root_dir / "output"
    work_dir = root_dir / "work"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)


def pull_config(client, job, root_dir, api_key):
    """Creates config.json, manifest.json and saves it at `root_dir`.

    Args:
        client (flywheel.Client): A Flywheel client
        job (flywheel.Job): A flywheel job object
        root_dir (Path-like): Path where to save the config.json
        api_key (str): Flywheel Api-key to be store in the config.json
    """
    gear = client.get_gear(job.gear_id).gear
    if api_key:
        if gear.inputs.get("api-key"):
            job["config"]["inputs"]["api-key"] = {
                "base": "api-key",
                "key": api_key,
            }

    # Dump to config file
    config_file = Path(root_dir) / "config.json"
    manifest_file = Path(root_dir) / "manifest.json"
    with open(config_file, "w") as fp:
        json.dump(job["config"], fp, indent=4)
    with open(manifest_file, "w") as fp:
        json.dump(dict(gear), fp, indent=4)
    return 0


def pull_inputs(client, job, root_dir):
    """Pull input files from Flywheel instance.

    Args:
        client (flywheel.Client): A Flywheel client
        job (flywheel.Job): A flywheel job object
        root_dir (Path-like): Path where to store the inputs files
    """
    inputs = job.config.get("inputs")
    input_dir = root_dir / "input"
    for k, v in inputs.items():
        log.info("Downloading %s...", k)
        if k == "api-key":
            continue
        (input_dir / k).mkdir(exist_ok=True)
        if v["base"] == "file":
            filename = v["location"]["name"]
            parent_id = v["hierarchy"]["id"]
            parent_type = v["hierarchy"]["type"]
            dest_path = str(input_dir / k / filename)
            download_fn = getattr(client, "download_file_from_" + parent_type)
            log.debug(
                "Downloading %s from %s (%s) to %s",
                filename,
                parent_type,
                parent_id,
                dest_path,
            )
            try:
                download_fn(parent_id, filename, str(input_dir / k / filename))
            except flywheel.rest.ApiException as e:
                if e.status == 404:
                    log.error("Input file doesn't exist")
                    return 1
    return 0


def pull_job_assets(client, job, root_dir, api_key):
    """Pull inputs and config.json.

    Args:
        client (flywheel.Client): A Flywheel client
        job (flywheel.Job): A flywheel job object
        root_dir (Path-like): Path where to save the assets
        api_key (str): Flywheel Api-key to be store in the config.json if needed
    """
    conf_ret = pull_config(client, job, root_dir, api_key)
    input_ret = pull_inputs(client, job, root_dir)
    if not (conf_ret or input_ret):
        log.info("Pulling assets for job %s - DONE", job.id)
        return 0
    return conf_ret + input_ret
