import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global edit
    edit = devcli_cmd("edit")


def test_simple():
    result = edit("config")
