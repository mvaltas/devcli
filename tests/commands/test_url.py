from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from devcli.core.cli import cli
from devcli.framework.error import MissConfError

runner = CliRunner()

url = lambda *params: runner.invoke(cli, ['url'] + list(params))


@pytest.fixture(autouse=True)
def setup():
    from devcli.config import Config
    from devcli.core import project_root
    # loads testing configuration
    Config().add_config(project_root('tests/fixtures/general.toml'))


def test_list():
    result = url('list')
    assert "devcli: https://github.com/mvaltas/devcli" in result.output
    assert "duck: https://duckduckgo.com" in result.output


def test_basic_search():
    result = url('search', 'duck')
    assert "duck: https://duckduckgo.com" in result.output


def test_partial_match_search():
    result = url('search', 'ck')
    assert "duck: https://duckduckgo.com" in result.output


def test_exact_match_open():
    with patch('devcli.utils.shell.run') as mock_run:
        url('open', 'duck')
        mock_run.assert_called_once_with("open 'https://duckduckgo.com'")


def test_partial_match_multiple_first_alphabetical_wins():
    with patch('devcli.utils.shell.run') as mock_run:
        url('open', 'g')
        mock_run.assert_called_once_with("open 'https://bing.com'")


def test_raises_error_if_no_key_is_found():
    result = url('open', 'undefined-key-in-configuration')
    assert result.exit_code != 0
    assert isinstance(result.exception, MissConfError)
