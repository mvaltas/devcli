from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def setup(devcli_cmd):
    global op
    op = devcli_cmd("op")


@patch("devcli.utils.one_password.capture")
def test_password(mock_capture):
    op("password", "--account", "personal", "devcli-test")

    mock_capture.assert_called_once()
    call_args = mock_capture.call_args[0][0]

    assert "op read --account" in call_args
    assert "op://Private/devcli-test/password"


@patch("devcli.utils.one_password.capture")
def test_credentials(mock_capture):
    op("credential", "--account", "personal", "devcli-test-api")

    mock_capture.assert_called_once()
    call_args = mock_capture.call_args[0][0]

    assert "op read --account" in call_args
    assert "op://Private/devcli-test-api/credential" in call_args
