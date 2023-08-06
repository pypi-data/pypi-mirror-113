"""Gear config module."""
import argparse
import json
import logging
import shutil
from pathlib import Path

from flywheel_gear_toolkit.utils.config import Config, ConfigValidationError
from flywheel_gear_toolkit.utils.manifest import Manifest, ManifestValidationError

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add gear config command."""
    parser = subparsers.add_parser(  # pylint: disable=line-too-long
        "config",
        parents=parents,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Gear config create or update.

        Create
        ------
        Run `fw gear config --create` to generate a default config from the
        manifest in your current folder.  If a manifest is not found in your
        current folder, you will see an error.

        Update
        ------
        Once the config has been generated either through
        `fw gear config --create` or by pulling a job with `fw job pull`,
        you can update configuration or input values in the manifest by
        passing the key and value as an argument to `fw gear config`.

        From within the gear directory (must contain manifest) run `fw gear
        config -h` to view the possible inputs/config you can pass into
        `fw gear config`

        """,
    )
    main_g = parser.add_argument_group(title="Gear config options")
    main_g.add_argument(
        "-c",
        "--create",
        help="""Create a config.json from default values of manifest.json.
        This doesn't populate any inputs, and all other arguments will be
         ignored when this option is specified""",
        action="store_true",
    )
    main_g.add_argument("--api-key", help="Add your api key to the config.json")

    # TODO: Move these to when either only gear config is called
    c_dict, i_dict = get_args(parser, (Path.cwd() / "manifest.json"))
    parser.set_defaults(
        func=gear_config,
        parser=parser,
        input_dict=i_dict,
        conf_dict=c_dict,
        help_func=parser.print_help,
        pwd=Path.cwd(),
    )
    return parser


def gear_config(  # pylint: disable=too-many-branches,too-many-return-statements
    args: argparse.Namespace,
) -> int:
    """Add main gear_config entry."""
    # Gear config create or update

    if args.create:
        saved = save_backup(args.pwd / "config.json")
        if saved:
            log.info(f"Config already exists, saved backup config to {saved.name}")

        manifest = _require_manifest(args.pwd)
        if not manifest:
            log.error("Need manifest in current dir to generate config.")
            return 1

        conf = Config.default_config_from_manifest(manifest)

        write_path = (args.pwd / "config.json").resolve()

        log.info(f"Config generated writing to {str(write_path)}")
        conf.to_json(str(write_path))
        return 0

    config = None
    try:
        log.info("Trying to load gear config.json")
        config = Config(path=(args.pwd / "config.json"))
    except ConfigValidationError as e:
        log.error(e)
        log.info("Try `fw gear config --create`")
        return 1

    log.debug(f"Current config {config}")

    if not config:
        log.warning("Couldn't find available config or input options. Exiting.")
        return 0

    if getattr(args, "api_key", None):
        log.info("Adding api-key input")
        config.add_input("api-key", args.api_key, type_="api-key")

    conf_dict = getattr(args, "conf_dict", {})
    input_dict = getattr(args, "input_dict", {})

    conf_update = {}
    if not conf_dict or not input_dict:
        log.warning("Could not find config and/or inputs.  Nothing will be updated.")
    else:
        manifest = _require_manifest(args.pwd)
        for key, val in vars(args).items():
            if val:
                if key in conf_dict:
                    # Configuration item
                    name = conf_dict.get(key).get("name")
                    conf_update[name] = val
                elif key in input_dict:
                    if not manifest:
                        log.error("Need manifest in current dir to update inputs.")
                        return 1
                    log.info(f"Adding input {key} at {str(val)}")
                    # Input item
                    name = input_dict.get(key)
                    base = manifest.inputs.get(name, {}).get("base", "file")
                    try:
                        config.add_input(name, str(val), type_=base)
                    except ValueError as e:
                        log.error(e)
                        return 1
                    populate_input_map(val, config.inputs[name]["location"]["path"])

    config.update_config(conf_update)
    config.to_json()
    return 0


def populate_input_map(local_path, docker_path):
    """Populate a map of local inputs to gear inputs."""
    input_map_f = Path("~/.cache/flywheel/input_map.json").expanduser()
    input_map = {}
    try:
        with open(input_map_f, "r") as fp:
            input_map = json.load(fp)
    except FileNotFoundError:
        input_map_f.parents[0].mkdir(parents=True, exist_ok=True)
        input_map_f.touch()
    except json.JSONDecodeError:
        log.warning("Can't decode input map")
    input_map.update({docker_path: local_path})

    with open(input_map_f, "w") as fp:
        json.dump(input_map, fp)


def save_backup(conf):
    """Helper function to save backup config.json."""
    if conf.exists() and conf.is_file():
        check_path = conf.parents[0] / "config.json.back"
        shutil.move(str(conf), str(check_path))
        return check_path
    return None


def get_args(parser, manifest_path):  # pylint: disable=too-many-locals
    """Parse manifest, add arguments for config and input to main argument parser.

    Note:
        The dictionary mapping of config and input options is for a use case where
        the argument name (`<arg_name>` below) is different than what is in the
        manifest (`<config_name>` and `<input_name>` below).  This is mainly for
        scenarios where a config or input value name is the same as an argument that
        has already been added to the parser.  E.g. `--timezone` is already an
        argument in the global python-cli parser, so if a gear needs to have a
        config value `timezone` this argument would need to be renamed before being
        added to the arg parser.

        Additionally, this may be implemented more in the future.

    Args:
        parser (argparse.ArgumentParser): parent argument parser

    Returns:
        tuple: tuple contianing:
            - config dictionary:
                {
                    <arg_name: str>: {                      # Default
                        'name': '<config_name: str>',
                        'default': <default_value: Any>
                    },
                    <arg_name: str>: {                      # No default
                        'name': '<config_name: str>'
                    }
                }
            - input dictionary:
                {<arg_name: str>: <input_name: str>}
    """
    # This is a bit of a hacky piece of code.  Since this is called before
    #   arguments are parsed, this gets called for each subcommand,
    #   here we check if the subcommand is not gear config, and if thats
    #   the case we don't attempt to add options from the manifest
    program = parser.prog.split(" ")
    if " ".join(program[-2:]) != "gear config":
        return None, None

    if not (manifest_path.exists() and manifest_path.is_file()):
        log.debug("Manifest not present in current dir.")
        return {}, {}
    manifest = Manifest(manifest_path)

    config = manifest.config
    inputs = manifest.inputs

    config_g = parser.add_argument_group(
        title="Configuration arguments",
        description="""Arguments for populating the configuration part of config.json.
        These are automatically populated with `fw gear config --create`""",
    )
    input_g = parser.add_argument_group(
        title="Input arguments",
        description="Arguments for populating the inputs section of config.json.",
    )

    config_dict = dict()
    input_dict = dict()

    for opt, val in config.items():
        conf_val = dict()
        conf_val["name"] = opt  # Store actual config name from manifest.json
        if "default" in val:
            conf_val["default"] = val.get("default")  # Add default value if provided
        arg_name, parsed_name, action, opt_help = handle_arg(opt, val)
        try:
            config_g.add_argument(f"--{arg_name}", action=action, help=opt_help)
        except argparse.ArgumentError as e:
            # Rename arg if necessary, see method docstring for details
            log.warning(
                f"Config option in manifest {e.argument_name} is already "
                "an argument for the CLI, flag will be renamed to "
                f"{arg_name}-config"
            )
            config_g.add_argument(f"--{arg_name}-config", action=action, help=opt_help)
            config_dict[f"{parsed_name}_config"] = conf_val  # Store arg name as key
        else:
            config_dict[f"{parsed_name}"] = conf_val

    # Set default values if present
    config_g.set_defaults(
        **{k: v.get("default") for k, v in config_dict.items() if v.get("default")}
    )

    for opt, val in inputs.items():
        if val.get("base") == "file":
            arg_name, parsed_name = _wrap_arg_name(opt)
            try:
                input_g.add_argument(f"--{arg_name}", help=val.get("description"))
            except argparse.ArgumentError as e:
                log.warning(
                    f"Input option in manifest {e.argument_name} is already an "
                    "argument for the CLI, flag will be renamed to"
                    "{arg_name}-config"
                )
                input_g.add_argument(
                    f"--{arg_name}-config", help=val.get("description")
                )
                input_dict[f"{parsed_name}_config"] = opt
            else:
                input_dict[parsed_name] = opt

    return config_dict, input_dict


def _wrap_arg_name(name):
    """Handle argument renaming weirdness with hyphens and underscores.

    Args:
        name (str): Argument to set

    Returns:
        tuple:
            - (str) name to pass into add_argument
            - (str) name returned from parse_args
    """
    name = name.strip()
    return (name.replace("_", "-"), name.replace("-", "_"))


def handle_arg(arg, val):
    """Handle an argument from a manifest.

    Args:
        arg (str): Config value name
        val (dict): Dictionary describing value, typ.
            ex.
                arg: "export_project"
                val:
                   {
                        "type": "boolean",
                        "description": "Ignore existing... Default: True",
                        "default": True
                    }

    Raises:
        ValueError: If argument cannot be added

    Returns:
        tuple: tuple contianing:
            - (str) name to pass into add_argument
            - (str) name returned from parse_args
            - argument parser action
            - help string
    """
    arg_name, parsed_name = _wrap_arg_name(arg)
    action = "store"
    opt_help = ""

    if "type" not in val:
        log.warning(
            f"Could not determine config type for value {arg}, "
            "please ensure `type` key is in manifest"
        )

    if val.get("type") == "boolean":
        action = "store_true"

    opt_help = val.get("description")

    return arg_name, parsed_name, action, opt_help


def _require_manifest(pwd):
    """Helper function to require presence of manifest."""
    try:
        manifest = Manifest(str(pwd / "manifest.json"))
    except (ManifestValidationError, FileNotFoundError):
        log.error(
            "Could not find manifest in current directory. "
            "Need manifest to know available input/config "
            "arguments for your gear."
        )
        return None
    return manifest
