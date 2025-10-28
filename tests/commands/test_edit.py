import pytest

from unittest.mock import patch, ANY


@pytest.fixture
def mock_exec():
    with patch("devcli.commands.edit.os.execvp") as mock:
        yield mock


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global edit
    edit = devcli_cmd("edit")


def test_edit_config_calls_editor(mock_exec):
    result = edit("config")
    mock_exec.assert_called_once_with("nvim", ["nvim", ANY])


def test_edit_command_calls_editor(mock_exec):
    result = edit("command", "placeholder")
    mock_exec.assert_called_once_with("nvim", ["nvim", ANY])
