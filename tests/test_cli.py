import re

from typer.testing import CliRunner

from devcli.core.cli import cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli, ['show-version'])
    assert re.match(r".*version\s\d+\.\d+\.\d+$", result.output) is not None

def test_default_to_help_if_command_not_found():
    result = runner.invoke(cli, [])
    assert "Usage: main [OPTIONS] COMMAND [ARGS]" in result.output

def test_passing_debug_changes_loglevel_to_debug(caplog):
    runner.invoke(cli, ['--debug', 'show-version'])
    assert any(record.levelname == "DEBUG" for record in caplog.records)

def test_passing_verbose_changes_loglevel_to_info(caplog):
    runner.invoke(cli, ['--verbose', 'show-version'])
    assert any(record.levelname == "INFO" for record in caplog.records)

def test_should_load_dynamic_commands():
    # example subcommand works because we have a .devcli in the root
    # of the project, tests of the subcommand 'example' itself
    # are in test_example.py
    result = runner.invoke(cli, ['example'])
    assert "ping" in result.output

def test_show_config():
    result = runner.invoke(cli, ['show-config'])
    assert '[devcli]' in result.output


def test_show_config_audit_log():
    result = runner.invoke(cli, ['show-config', '--explain'])
    assert re.search(r'conf/defaults\.toml', result.output)
    assert re.search(r'\.config/devcli/devcli\.toml', result.output)
    assert re.search(r'\.devcli/devcli\.toml', result.output)
