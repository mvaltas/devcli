"""
devcli.framework is a collection of helper functions for tool commands
so that they don't have to reimplement common tasks related to a command
work.
"""
import sys

import typer
from rich import print


def new(description: str = None) -> typer.Typer:
    """
    The base of starting a new dynamic command. It
    returns the basic Typer type for command declaration.
    :returns: a typer.Typer
    """
    return typer.Typer(help=description, no_args_is_help=True)


def echo(msg: str):
    """
    Just print a message into the terminal.
    It uses rich.print() which allows for color tagging like [red]message[/red].
    :param msg: A str with the message
    """
    print(msg)


def error(msg: str):
    """
    Print a message in red
    """
    print(f"[red]{msg}[/red]")


def warn(msg: str):
    """
    Prints a message in yellow
    """
    print(f'[yellow]{msg}[/yellow]')


def notice(msg: str):
    """
    Prints a message in cyan
    """
    print(f'[cyan]{msg}[/cyan]')


def stop(msg: str, exit_code: int = 1):
    """
    Prints a message in red if defined and stops the execution
    :param msg:
    :param exit_code: Optional exit number, defaults to 1
    """
    if msg is not None:
        error(msg)

    sys.exit(exit_code)
