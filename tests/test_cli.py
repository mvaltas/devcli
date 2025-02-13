import re

import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global devcli
    devcli = devcli_cmd()


def test_version():
    result = devcli("show-version")
    assert re.match(r".*version\s\d+\.\d+\.\d+$", result.output) is not None


def test_default_to_help_if_command_not_found():
    result = devcli()
    assert "Usage: devcli [OPTIONS] COMMAND [ARGS]" in result.output


def test_passing_debug_changes_loglevel_to_debug(caplog):
    devcli("--debug", "show-version")
    assert any(record.levelname == "DEBUG" for record in caplog.records)


def test_passing_debug_short_flag_changes_loglevel_to_debug(caplog):
    devcli("-d", "show-version")
    assert any(record.levelname == "DEBUG" for record in caplog.records)


def test_passing_verbose_changes_loglevel_to_info(caplog):
    devcli("--verbose", "show-version")
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_passing_verbose_short_flag_changes_loglevel_to_info(caplog):
    devcli("-v", "show-version")
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_should_load_dynamic_commands():
    # example subcommand works because we have a .devcli in the root
    # of the project, tests of the subcommand 'example' itself
    # are in test_example.py
    result = devcli("example")
    assert "ping" in result.output


def test_show_config():
    result = devcli("show-config")
    assert "[devcli]" in result.output


def test_show_config_audit_log():
    result = devcli("show-config", "--explain")
    assert re.search(r"conf/defaults\.toml", result.output)
    assert re.search(r"\.config/devcli/devcli\.toml", result.output)
    assert re.search(r"\.devcli/devcli\.toml", result.output)
