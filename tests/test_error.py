from devcli.framework.errors import MissConfError


def test_miss_conf_error_message():
    error = MissConfError("subcommand", "configuration_key", "example_value")
    expected_message = (
        "Missing entry 'configuration_key' on 'subcommand'.\n"
        "Ensure you have the following in your configuration:\n\n"
        "[subcommand]\n"
        "configuration_key = example_value\n"
    )
    assert str(error) == expected_message
