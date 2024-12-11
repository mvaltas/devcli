import re

from typer.testing import CliRunner

from devcli.core.cli import cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli, ['version'])
    assert re.match(r".*version\s\d+\.\d+\.\d+$", result.output) is not None

def test_default_to_help_if_command_not_found():
    result = runner.invoke(cli, [])
    assert "Usage: main [OPTIONS] COMMAND [ARGS]" in result.output

def test_passing_debug_changes_loglevel_to_debug(caplog):
    runner.invoke(cli, ['--debug', 'version'])
    assert any(record.levelname == "DEBUG" for record in caplog.records)

def test_passing_verbose_changes_loglevel_to_info(caplog):
    runner.invoke(cli, ['--verbose', 'version'])
    assert any(record.levelname == "INFO" for record in caplog.records)

def test_should_load_dynamic_commands():
    result = runner.invoke(cli, ['--debug', 'example'])
    assert "asdf" in result.output