import logging

import typer
from rich import print
from typer import Context

from devcli.config import Config
from devcli.core import (project_root,
                         traverse_load_dynamic_commands,
                         load_dynamic_commands)

cli = typer.Typer(add_completion=False)

boot_conf = Config()

if boot_conf['devcli.enable_builtin_commands']:
    load_dynamic_commands(cli, project_root('devcli/commands'))

traverse_load_dynamic_commands(cli, '.devcli')


@cli.command(hidden=True)
def show_version():
    """
    Show devcli version which is defined in pyproject.toml file

    :return: tool.poetry.version
    """
    project_conf = Config().add_config(project_root('pyproject.toml'))
    print(f'devcli version {project_conf['tool.poetry.version']}')


@cli.command(hidden=True)
def show_config():
    """
    Will show all configuration parsed by devcli
    """
    print(Config())


@cli.callback(invoke_without_command=True)
def main(ctx: Context,
         debug: bool = typer.Option(False, "--debug", help="Enable debug log"),
         verbose: bool = typer.Option(False, "--verbose", help="Enable info log")):
    logger = logging.getLogger()
    # set global log level
    if debug:
        logger.setLevel(level=logging.DEBUG)
        logging.debug("Debug logging enabled")
    elif verbose:
        logger.setLevel(level=logging.INFO)
        logging.info("Verbose mode enabled")

    # call help on the absence of a command
    if ctx.invoked_subcommand is None:
        logger.info("no subcommand given, defaulting to help message")
        typer.echo(ctx.get_help())
        raise typer.Exit()

    logger.debug('setting configuration in the subcommand context')
    ctx.obj = Config()
