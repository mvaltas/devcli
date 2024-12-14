"""
devcli.framework is a collection of helper functions for tool commands
so that they don't have to reimplement common tasks related to a command
work.
"""

import sys

import typer

from devcli.framework.console import error


def new(description: str = None) -> typer.Typer:
    """
    The base of starting a new dynamic command. It
    returns the basic Typer type for command declaration.
    :returns: a typer.Typer
    """
    return typer.Typer(help=description, no_args_is_help=True)


def stop(msg: str, exit_code: int = 1):
    """
    Prints a message in red if defined and stops the execution
    :param msg:
    :param exit_code: Optional exit number, defaults to 1
    """
    if msg is not None:
        error(msg)

    sys.exit(exit_code)
