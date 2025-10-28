"""
devcli.framework is a collection of helper functions for tool commands
so that they don't have to reimplement common tasks related to a command
work.
"""

import logging
import sys
from pathlib import Path

import typer
import inspect

import devcli.framework.console as console
from devcli.core.cli import OrderedGroup

_logger = logging.getLogger()


def new(description: str = None, **kwargs) -> typer.Typer:
    """
    The base of starting a new dynamic command. It
    returns the basic Typer type for command declaration.
    :returns: a typer.Typer
    """
    _logger.info(f"creating new command description:{description}")
    return typer.Typer(help=description, no_args_is_help=True, cls=OrderedGroup, **kwargs)


def stop(msg: str = "Error", exit_code: int = 1):
    """
    Prints a message in red if defined and stops the execution
    :param msg:
    :param exit_code: Optional exit number, defaults to 1
    """
    _logger.info(f"stopping executing msg:{msg} exit_code:{exit_code}")
    console.error(msg)
    sys.exit(exit_code)


def logger(name: str = None) -> logging.Logger:
    """
    Returns an instance of logging.logger set to file name of the
    caller.

    :return:
    """
    if name is None:
        caller_frame = inspect.stack()[1]
        name = f"command:{Path(caller_frame[1]).stem}"

    _logger.debug(f"returning a new logger to command ({name})")
    return logging.getLogger(name)
