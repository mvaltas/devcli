import importlib.util
import logging
import os
from pathlib import Path

from typer import Typer

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEVCLI_LOGLEVEL = os.environ.get('DEVCLI_LOGLEVEL', "WARNING")

# user default configuration path
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config' )

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.getLevelName(DEVCLI_LOGLEVEL.upper()))

# debug only available if DEVCLI_LOGLEVEL is defined as "debug"
_init_logger = logging.getLogger('devcli.core.__init__')



def project_root(filename=None) -> Path:
    """
    Should return the directory in which devcli is contained, which
    is mostly the entry point for defaults and supporting code.
    If filename is given it will append project_root() into filename.
    """
    # this is predicated on the fact we know where this file is
    parent = Path(__file__).resolve().parent.parent.parent
    _init_logger.debug(f"project_root={parent}")
    if filename is None:
        return parent
    else:
        return parent / filename


def load_dynamic_commands(app: Typer, directory: Path):
    if not directory.exists():
        _init_logger.debug(f"couldn't find dir {directory}")
        return

    for file in directory.glob("*.py"):
        _init_logger.debug(f"found file: {file}")
        module_name = file.stem  # Get the file name without '.py'
        _init_logger.debug(f'module: {module_name}')
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        _init_logger.debug(f'executing module: {module}')
        spec.loader.exec_module(module)
        if hasattr(module, 'cli'):
            _init_logger.debug(f'"cli" attribute found, adding command: {module_name}')
            app.add_typer(module.cli, name=module_name)


def traverse_search(target: str | Path, start: str | Path = Path.cwd()) -> [str]:
    _init_logger.debug(f'traverse_search[{target}, {start}]')

    search_start_from = Path(start)
    if search_start_from.is_file():
        _init_logger.debug(f'start was a file, converting to directory')
        search_start_from = search_start_from.parent

    target = Path(target).name
    _init_logger.debug(f'start search for {target}, from {search_start_from}')

    found = [] # results
    # Traverse up the directory tree
    while True:
        path_to_check = search_start_from / target
        if path_to_check.exists():
            found.append(str(path_to_check))

        if search_start_from.parent == search_start_from:  # Root directory reached
            break
        search_start_from = search_start_from.parent

    return found

# def load_default_commands(cli: Typer) -> None:
#     """
#     This function is in charge of loading the default commands for devcli.
#     We don't use the dynamic loading in this case to save time and control
#     which ones should be loaded or not.
#
#     The command will be defined as its name, for example 'devcli.command.ci' will
#     be defined as 'ci'
#
#     :param cli: a Typer object that allow for `.add_typer` calls
#     :return: None
#     """
#     # default commands that can be reused
#     from devcli.command import (
#         ci,
#         op,
#     )
#     commands = [ci, op]
#     for c in commands:
#         _init_logger.debug(f'loading default command ({c.__name__})')
#         cli.add_typer(c.cli, name=c.__name__.split('.')[-1])
