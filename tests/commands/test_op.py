import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global op
    op = devcli_cmd("op")


def test_password():
    result = op("password", "--account", "personal", "devcli-test")
    assert result.output in "this-is-a-test-password\n"


def test_credentials():
    result = op("credential", "--account", "personal", "devcli-test-api")
    assert result.output in "some-sensitive-api-value\n"
