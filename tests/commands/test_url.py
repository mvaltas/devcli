from unittest.mock import patch

import pytest

from devcli.framework.errors import MissConfError


@pytest.fixture(autouse=True)
def setup(setup_cmd):
    from devcli.config import Config
    from devcli.core import project_root

    # loads testing configuration
    Config().add_config(project_root("tests/fixtures/general.toml"))

    global url
    url = setup_cmd("url")


def test_list():
    result = url("list")
    assert "https://github.com/mvaltas/devcli" in result.output
    assert "https://duckduckgo.com" in result.output


def test_basic_search():
    result = url("search", "duck")
    assert "duck: https://duckduckgo.com" in result.output


def test_partial_match_search():
    result = url("search", "ck")
    assert "duck: https://duckduckgo.com" in result.output


def test_exact_match_open():
    with patch("devcli.utils.shell.run") as mock_run:
        url("open", "duck")
        mock_run.assert_called_once_with("open 'https://duckduckgo.com'")


def test_partial_match_multiple_first_alphabetical_wins():
    with patch("devcli.utils.shell.run") as mock_run:
        url("open", "g")
        mock_run.assert_called_once_with("open 'https://bing.com'")


def test_raises_error_if_no_key_is_found():
    result = url("open", "undefined-key-in-configuration")
    assert result.exit_code != 0
    assert isinstance(result.exception, MissConfError)
