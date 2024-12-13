import pytest
from typer.testing import CliRunner

from devcli.core.cli import cli

runner = CliRunner()

def invoke_command(cmd: str = None):
    # pre-prepare a command that will be invoked several times
    # with different parameters
    return lambda *params: runner.invoke(cli, ([cmd] if cmd else []) + list(params))

@pytest.fixture
def setup_cmd():
    """
    This fixture allows for reusing of invoke_command on Typer tests, in the tests
    you can set up without having to worry about the invoke or CliRunner()

    Example::

        @pytest.fixture(autouse=True)
        def setup(setup_cmd):
            global cmd_under_test
            cmd_under_test = setup_cmd("cmd-under-test")

        def test_something():
            result = cmd_under_test("options", "parameters")
            assert "expected output" == result.output
    """
    return invoke_command