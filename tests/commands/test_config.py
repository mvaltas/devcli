from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    from devcli.config import Config
    from devcli.core import project_root

    # loads testing configuration
    Config().add_config(project_root("tests/fixtures/general.toml"))

    global config
    config = devcli_cmd("config")


def test_get():
    result = config("get", "devcli.key")
    assert "value" in result.output
