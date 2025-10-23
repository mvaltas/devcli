import pytest

from unittest.mock import patch
import devcli.framework.console as console

MESSAGE = "Hello, World!"


@pytest.fixture
def mock_print():
    with patch("devcli.framework.console.print") as mock:
        yield mock


def assert_print(mock, color=None):
    if color:
        mock.assert_called_once_with(f"[{color}]{MESSAGE}[/{color}]")
    else:
        mock.assert_called_once_with(f"{MESSAGE}")


def test_echo(mock_print):
    console.echo(MESSAGE)
    assert_print(mock_print)


def test_info(mock_print):
    console.info(MESSAGE)
    assert_print(mock_print, color="cyan")


def test_warn(mock_print):
    console.warn(MESSAGE)
    assert_print(mock_print, color="yellow")


def test_error(mock_print):
    console.error(MESSAGE)
    assert_print(mock_print, color="red")


def test_simple_grid(mock_print):
    grid = [["Row A", "Row B"]]
    console.table(grid)

    argument = mock_print.call_args.args[0]
    full_name = ".".join([argument.__module__, argument.__class__.__name__])

    assert full_name == "rich.table.Table"


def test_simple_table(mock_print):
    grid = [["Col A", "Col B"], ["Row A", "Row B"]]
    console.table(grid)

    argument = mock_print.call_args.args[0]
    full_name = ".".join([argument.__module__, argument.__class__.__name__])

    assert full_name == "rich.table.Table"
