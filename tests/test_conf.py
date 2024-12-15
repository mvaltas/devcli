import pytest

from devcli.core import project_root


@pytest.fixture(autouse=True)
def setup():
    from devcli.config import Config

    # force reset of singleton for testing
    Config._instance = None
    global conf
    conf = Config().add_config(project_root("tests/fixtures/general.toml"))


def test_it_parses_one_conf_file():
    assert conf["devcli"]["key"] == "value"


def test_it_adds_configurations_of_other_files():
    assert conf["devcli"]["key"] == "value"
    assert conf["a_specific_configuration"] is None

    conf.add_config(project_root("tests/fixtures/specific.toml"))

    assert conf["devcli"]["key"] == "value"
    assert conf["a_specific_configuration"]["key"] == "value"


def test_last_added_configuration_overrides_values():
    # from the initialization of general.toml
    assert conf["overridable_configuration"]["key"] == "general_value"

    # load specific configuration
    conf.add_config(project_root("tests/fixtures/specific.toml"))
    assert conf["overridable_configuration"]["key"] == "specific_value"

    # load general configuration again
    conf.add_config(project_root("tests/fixtures/general.toml"))
    assert conf["overridable_configuration"]["key"] == "general_value"


def test_it_ignores_if_asked_to_load_non_existent_file():
    # non-existent file
    conf.add_config("this_file_does_not_exists")
    # does not affect the configuration
    assert conf["devcli"]["key"] == "value"


def test_it_accepts_fetch_through_path_str():
    assert conf["devcli.key"] == "value"
    assert conf["overridable_configuration.key"] == "general_value"


def test_audit_should_list_files_loaded():
    assert conf.audit()[project_root("tests/fixtures/general.toml")] is not None


def test_audit_should_be_immutable():
    config_key = project_root("tests/fixtures/general.toml")
    audit = conf.audit()
    # config is listed in audit
    assert audit[config_key] is not None
    # dict has value altered
    audit[config_key] = None
    # fetching audit again does not alter the original dict
    assert conf.audit()[config_key] is not None


def test_files_returns_files_loaded():
    gen_config = project_root("tests/fixtures/general.toml")
    spec_config = project_root("tests/fixtures/specific.toml")
    # general was loaded in setup, but specific not
    assert gen_config in conf.files()
    assert spec_config not in conf.files()
    # load specific
    conf.add_config(spec_config)
    # and now it is listed in files()
    assert spec_config in conf.files()
