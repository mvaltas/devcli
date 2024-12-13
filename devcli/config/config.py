import logging
from pathlib import Path
from typing import Any

import toml

from devcli.core import project_root, XDG_CONFIG_HOME


class Config:
    logger = logging.getLogger(__name__)
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls.logger.info(f"loading Config singleton")

            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)

            cls._instance._config = {}  # init config holder empty
            cls._instance._audit = []  # history of what was loaded

            cls.logger.info("loading default configuration locations")
            # load defaults from devcli package
            cls._instance.add_config(project_root() / "conf" / "defaults.toml")
            # load global user config it can override defaults.toml
            cls._instance.add_config(XDG_CONFIG_HOME / "devcli" / "devcli.toml")

        return cls._instance

    def add_config(self, config_file: str | Path):
        if Path(config_file).is_file():
            with open(config_file) as file:
                self.logger.debug(f"loading {config_file} data")
                config_contents = toml.load(file)
                self._audit.append({config_file: config_contents})
                self.logger.debug(f"configuration contents: {config_contents}")
                self.merge_update(self._config, config_contents)
        else:
            self.logger.warning(f"{config_file} is not a file or does not exist")

        return self

    def merge_update(self, source: dict, overrides: dict):
        """
        It merges similar keys in a deep dict structure, preserving
        keys unless they are exactly the same, in which case their
        values will be overwritten.
        """
        for key, value in overrides.items():
            if (
                isinstance(value, dict)
                and key in source
                and isinstance(source[key], dict)
            ):
                self.merge_update(source[key], value)
            else:
                source[key] = value

    def audit(self):
        """
        Returns a list with the files and content that was loaded
        into the configuration object for debug purposes
        """
        return self._audit

    def __getitem__(self, item: str) -> Any:
        self.logger.debug(f"getitem:{item}")
        if "." in item:
            keys = item.split(".")
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
        self.logger.debug("dumping config representation with toml.dumps()")
        return toml.dumps(self._config)
