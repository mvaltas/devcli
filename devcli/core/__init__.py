import importlib.util
import logging
import os
import sys
from pathlib import Path

from typer import Typer

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEVCLI_LOGLEVEL = os.environ.get('DEVCLI_LOGLEVEL', "WARNING")

# user default configuration path
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.getLevelName(DEVCLI_LOGLEVEL.upper()))

# debug only available if DEVCLI_LOGLEVEL is defined as "debug"
logger = logging.getLogger('devcli.core.__init__')


def project_root(filename=None) -> Path:
    """
    Should return the directory in which devcli is contained, which
    is mostly the entry point for defaults and supporting code.
    If filename is given it will append project_root() into filename.
    """
    # this is predicated on the fact we know where this file is
    parent = Path(__file__).resolve().parent.parent.parent
    logger.debug(f"project_root={parent}")
    if filename is None:
        return parent
    else:
        return parent / filename


def load_dynamic_commands(app: Typer, directory: Path):
    """
    scan a given directory for .py files and check if they
    contain the attribute 'cli', if so, it will consider
    a subcommand and add to Typer dynamically.
    """
    logger.debug(f"load_dynamic_commands:{directory}")
    if not directory.exists():
        logger.debug(f"couldn't find dir {directory}")
        return

    # adds directory as part of the loader path, this
    # allows commands to use relative import for their
    # own functions
    if directory not in sys.path:
        sys.path.insert(0, str(directory))

    for file in directory.glob("*.py"):
        logger.debug(f"found file: {file}")
        module_name = file.stem  # Get the file name without '.py'
        logger.debug(f'module: {module_name}')
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        logger.debug(f'executing module: {module}')
        spec.loader.exec_module(module)
        if hasattr(module, 'cli'):
            logger.debug(f'"cli" attribute found, adding as a subcommand: {module_name}')
            app.add_typer(module.cli, name=module_name)


def traverse_search(target: str | Path, start: str | Path = Path.cwd()) -> [Path]:
    """
    Given a target and a start point, it will traverse upwards the directory
    tree until getting to root directory and return a list of the
    locations where 'target' was found.
    """
    logger.debug(f'traverse_search[{target}, {start}]')

    search_start_from = Path(start)
    if search_start_from.is_file():
        logger.debug(f'start was a file, converting to directory')
        search_start_from = search_start_from.parent

    target = Path(target).name
    logger.debug(f'start search for {target}, from {search_start_from}')

    found = []  # results
    # Traverse up the directory tree
    while True:
        path_to_check = search_start_from / target
        if path_to_check.exists():
            found.append(path_to_check)

        if search_start_from.parent == search_start_from:  # Root directory reached
            break
        search_start_from = search_start_from.parent

    return found


def traverse_load_dynamic_commands(app: Typer, subcommand_dir: str, start: Path = Path.cwd()):
    """
    Uses traverse_search to load commands dynamically
    """
    directories = traverse_search(subcommand_dir, start)
    for d in directories:
        load_dynamic_commands(app, d)
