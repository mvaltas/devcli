from typer.testing import CliRunner

from devcli.core.cli import cli

runner = CliRunner()

example = lambda *params: runner.invoke(cli, ['example'] + list(params))

def test_ping():
    result = example('ping')
    assert result.output == "PONG!\n"

def test_hello():
    result = example('hello', 'Daniel')
    assert result.output == "Hello, Daniel!\n"

def test_hello_with_rainbow():
    # it will accept the flag but won't actually use colors
    # given the test environment (I think).
    result = example('hello', 'Marco', '--rainbow')
    assert result.output == 'Hello, Marco!\n'

def test_hello_text_example():
    result = example('text')
    for msg in ['echo(msg)', 'warn(msg)', 'notice(msg)', 'error(msg)']:
        assert msg in result.output

def test_config_example():
    result = example('config')
    assert "Default devcli config:" in result.output