import pytest
from unittest.mock import patch

from devcli.utils.one_password import OnePassword


@pytest.fixture
def one_password():
    return OnePassword(account="test-account", vault="TestVault")


def test_init_sets_account_and_vault():
    op = OnePassword(account="test-account", vault="TestVault")
    assert op.account == "--account test-account"
    assert op.vault == "TestVault"


def test_init_default_vault():
    op = OnePassword(account="test-account")
    assert op.account == "--account test-account"
    assert op.vault == "Private"


@patch("devcli.utils.one_password.capture")
def test_read_calls_op_read_with_correct_args(mock_capture, one_password):
    mock_capture.return_value = "secret-value\n"

    result = one_password.read("TestVault/test-item/field")

    mock_capture.assert_called_once_with(
        "op read --account test-account 'op://TestVault/test-item/field'"
    )
    assert result == "secret-value"


@patch("devcli.utils.one_password.capture")
def test_credential_calls_read_with_credential_path(mock_capture, one_password):
    mock_capture.return_value = "api-key-value\n"

    result = one_password.credential("api-key")

    mock_capture.assert_called_once_with(
        "op read --account test-account 'op://TestVault/api-key/credential'"
    )
    assert result == "api-key-value"


@patch("devcli.utils.one_password.capture")
def test_password_calls_read_with_password_path(mock_capture, one_password):
    mock_capture.return_value = "secure-password\n"

    result = one_password.password("login-item")

    mock_capture.assert_called_once_with(
        "op read --account test-account 'op://TestVault/login-item/password'"
    )
    assert result == "secure-password"


@patch("devcli.utils.one_password.capture")
def test_login_calls_read_with_login_path(mock_capture, one_password):
    mock_capture.return_value = "username@example.com\n"

    result = one_password.login("login-item")

    mock_capture.assert_called_once_with(
        "op read --account test-account 'op://TestVault/login-item/login'"
    )
    assert result == "username@example.com"


@patch("devcli.utils.one_password.capture")
def test_read_strips_newline_from_result(mock_capture, one_password):
    mock_capture.return_value = "value-with-newline\n"

    result = one_password.read("TestVault/item/field")

    assert result == "value-with-newline"
    assert not result.endswith("\n")


@patch("devcli.utils.one_password.capture")
def test_item_get(mock_capture, one_password):

    one_password.item_get(item="test-item", fields="password")

    mock_capture.assert_called_once_with(
        "op items get --account test-account --vault 'TestVault' "
        "--reveal --fields='password' test-item"
    )


@patch("devcli.utils.one_password.OnePassword.logger")
@patch("devcli.utils.one_password.capture")
def test_logging_debug_messages(mock_capture, mock_logger, one_password):
    mock_capture.return_value = "test-value\n"

    one_password.read("TestVault/item/field")

    mock_logger.debug.assert_called_with("read key=TestVault/item/field")
