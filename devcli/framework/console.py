from typing import List

from rich.table import Table
from rich.box import SQUARE
from rich import print
from rich import json as rjson


def echo(msg: str, *args, **kwargs):
    """
    Just print a message into the terminal.
    It uses rich.print() which allows for color tagging like [red]message[/red].
    :param msg: A str with the message
    """
    print(msg, *args, **kwargs)


def json(msg: str):
    """
    Print a json result
    """
    print(rjson.JSON(msg))


def error(msg: str):
    """
    Print a message in red
    """
    print(f"[red]{msg}[/red]")


def warn(msg: str):
    """
    Prints a message in yellow
    """
    print(f"[yellow]{msg}[/yellow]")


def info(msg: str):
    """
    Prints a message in cyan
    """
    print(f"[cyan]{msg}[/cyan]")


def banner(msg: str):
    """Uses a table to make a boxed banner"""
    table([[msg]], True)


def table(table: List[List[str]] = [[]], as_grid: bool = False):
    """
    Prints a simple table, for complex tables use rich.Table directly.

    First element will be used as column and the the rest as rows.
    For example:
        [
            ["Col  A", "Col  B"],
            ["Row 1A", "Row 1B"],
            ["Row 2A", "Row 2B"]
        ]

    as_grid: bool
    """
    rich_table = None
    table_copy = table.copy()  # avoid altering param

    # do nothing with an empty table
    if len(table_copy) == 0:
        return
    elif as_grid:
        rich_table = Table(show_lines=True, show_header=False, box=SQUARE)
    else:
        rich_table = Table(show_lines=True, box=SQUARE)

    if not as_grid:
        # use the cols given, also remove it
        cols = table_copy.pop(0)
        for c in cols:
            rich_table.add_column(c)

    # only rows should be remaining
    for r in table_copy:
        rich_table.add_row(*r)

    echo(rich_table)
