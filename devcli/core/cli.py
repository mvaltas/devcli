import logging
import pathlib

import typer
from typer import Context
from rich import print

from devcli.core import project_root, load_dynamic_commands #, load_default_commands
from devcli.config import Config

cli = typer.Typer(add_completion=False)

#load_default_commands(cli)
load_dynamic_commands(cli, pathlib.Path('.devcli'))

@cli.command()
def version():
    """
    Show devcli version which is defined in pyproject.toml file
    :return: tool.poetry.version
    """
    project_conf = Config().add_config(project_root('pyproject.toml'))
    print(f'devcli version {project_conf['tool.poetry.version']}')


@cli.callback(invoke_without_command=True)
def main(ctx: Context,
         debug: bool = typer.Option(False, "--debug", help="Enable debug log"),
         verbose: bool = typer.Option(False, "--verbose", help="Enable info log")):
    """
    Main callback that handles global options for devcli. It also setups context with config
    available for other commands.
    """
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
        typer.echo(ctx.get_help())
        raise typer.Exit()

    ctx.obj = Config()
