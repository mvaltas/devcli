from typer import Typer

from unittest.mock import patch
import devcli.framework.base as base


def test_new_creates_typer_instance():
    typer_instance = base.new("Test description")
    assert isinstance(typer_instance, Typer)


def test_stop_prints_error_and_exits():
    with patch("devcli.framework.console.error") as mock_error, patch(
        "sys.exit"
    ) as mock_exit:
        base.stop("Custom error message", 2)
        mock_error.assert_called_once_with("Custom error message")
        mock_exit.assert_called_once_with(2)


def test_stop_has_default_error_message():
    with patch("devcli.framework.console.error") as mock_error, patch(
        "sys.exit"
    ) as mock_exit:
        base.stop(exit_code=2)
        mock_error.assert_called_once_with("Error")
        mock_exit.assert_called_once_with(2)


def test_returns_logger_with_caller_file_name():
    with patch("inspect.stack") as mock_stack:
        mock_stack.return_value = [
            None,
            (
                "frame",
                ".devcli/filename",
                "lineno",
                "function",
                "code_context",
                "index",
            ),
        ]
        log = base.logger()
        assert log.name == "command:filename"


def test_return_logger_with_name_given():
    log = base.logger("test-logger")
    assert log.name == "test-logger"
