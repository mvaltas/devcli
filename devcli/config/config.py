import logging
import os.path
from pathlib import Path
from typing import Any

import toml

from devcli.core import project_root, traverse_search, XDG_CONFIG_HOME


class Config:
    logger = logging.getLogger(__name__)
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls.logger.debug(f'loading Config')

            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)

            cls._instance._config = {}  # init config holder empty

            # load defaults from devcli package
            cls._instance.add_config(project_root() / "conf" / "defaults.toml")
            # load global user config it can override defaults.toml
            cls._instance.add_config(XDG_CONFIG_HOME / "devcli" / "conf.toml")

            # standard up dir traverse looking for configuration files
            for config_file in reversed(traverse_search('devcli.toml')):
                cls._instance.add_config(config_file)

        return cls._instance

    def add_config(self, config_file: str | Path):
        if Path(config_file).is_file():
            with open(config_file) as file:
                self.logger.debug(f'loading {config_file} data')
                self._config.update(toml.load(file))
        else:
            self.logger.warning(f'{config_file} is not a file or does not exist')

        return self

    def __getitem__(self, item: str) -> Any:
        self.logger.debug(f'getitem:{item}')
        if "." in item:
            keys = item.split('.')
            level = self._config
            for key in keys:
                if isinstance(level, dict) and key in level:
                    level = level[key]
                else:
                    return None
            return level
        else:
            return self._config.get(item, None)

    def __repr__(self):
        return toml.dumps(self._config)