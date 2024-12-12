import logging

import typer
from rich import print
from typer import Context

from devcli.config import Config
from devcli.core import (project_root,
                         traverse_load_dynamic_commands,
                         traverse_search,
                         load_dynamic_commands)

cli = typer.Typer(add_completion=False)

# config is a singleton to be
# available to all parts of the system
boot_conf = Config()

# load user defined configurations in opposite order
for d in reversed(traverse_search('.devcli')):
    boot_conf.add_config(d / 'devcli.toml')

# should we load our own builtin commands?
if boot_conf['devcli.enable_builtin_commands']:
    load_dynamic_commands(cli, project_root('devcli/commands'))

# load use defined commands
traverse_load_dynamic_commands(cli, '.devcli')

@cli.command(hidden=True)
def show_version():
    """
    Show devcli version which is defined in pyproject.toml file

    :return: tool.poetry.version
    """
    project_conf = boot_conf.add_config(project_root('pyproject.toml'))
    print(f'devcli version {project_conf['tool.poetry.version']}')


@cli.command(hidden=True)
def show_config(explain: bool = False):
    """
    Display the current configuration parsed by devcli.

    If the `explain` parameter is set to True, the function will provide a detailed explanation
    of the configuration files that were loaded, including the order in which they were processed
    and any overrides that occurred.

    Args:
        explain (bool, optional): If True, provide a detailed explanation of the configuration
                                  loading process. Defaults to False.
    """
    if explain:
        print("[cyan]Explaining configurations:[/cyan]")
        print(boot_conf.audit())
    else:
        print(boot_conf)


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
