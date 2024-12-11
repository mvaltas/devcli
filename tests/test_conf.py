from devcli.config import Config
from devcli.core import project_root


def test_it_parses_one_conf_file():
    config_file = project_root('tests/fixtures/general.toml')
    conf = Config().add_config(config_file)
    assert conf['devcli']['key'] == 'value'


def test_it_adds_configurations_of_other_files():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    assert conf['devcli']['key'] == 'value'
    assert conf['a_specific_configuration'] is None

    conf.add_config(project_root('tests/fixtures/specific.toml'))
    assert conf['devcli']['key'] == 'value'
    assert conf['a_specific_configuration']['key'] == 'value'


def test_last_added_configuration_overrides_values():
    # load general configuration
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    assert conf['overridable_configuration']['key'] == 'general_value'

    # load specific configuration
    conf.add_config(project_root('tests/fixtures/specific.toml'))
    assert conf['overridable_configuration']['key'] == 'specific_value'

    # load general configuration again
    conf.add_config(project_root('tests/fixtures/general.toml'))
    assert conf['overridable_configuration']['key'] == 'general_value'


def test_it_ignores_if_asked_to_load_non_existent_file():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    # non-existent file
    conf.add_config('this_file_does_not_exists')
    # does not affect the configuration
    assert conf['devcli']['key'] == 'value'


def test_it_accepts_fetch_through_path_str():
    conf = Config().add_config(project_root('tests/fixtures/general.toml'))
    assert conf['devcli.key'] == 'value'
    assert conf['overridable_configuration.key'] == 'general_value'
