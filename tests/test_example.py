import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global example
    example = devcli_cmd("example")


def test_ping():
    result = example("ping")
    assert result.output == "PONG!\n"


def test_hello():
    result = example("hello", "Daniel")
    assert result.output == "Hello, Daniel!\n"


def test_hello_with_rainbow():
    # it will accept the flag but won't actually use colors
    # given the test environment (I think).
    result = example("hello", "Marco", "--rainbow")
    assert result.output == "Hello, Marco!\n"


def test_hello_text_example():
    result = example("text")
    expected_output = (
        "This is a cmd.echo(msg)\n"
        "This is a cmd.info(msg)\n"
        "This is a cmd.warn(msg)\n"
        "This is a cmd.error(msg)\n"
        "┌────────────────┬────────────────┐\n"
        "│ This is        │ a simple table │\n"
        "├────────────────┼────────────────┤\n"
        "│ With one value │ and another    │\n"
        "└────────────────┴────────────────┘\n"
    )
    assert result.output in expected_output


def test_config_example():
    result = example("config")
    assert "Default devcli config:" in result.output
