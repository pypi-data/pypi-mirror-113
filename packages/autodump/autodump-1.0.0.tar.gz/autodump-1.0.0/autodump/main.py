# -*- coding: utf-8 -*-

import inspect
import os
import yaml

from .medium import *


class Autodumper:
    def __init__(self, space, config=None, config_path="autodump.yaml"):
        if not ((config_path is None) ^ (config is None)):
            raise Exception("Either config or config_path (and not all) should be specified. ")
        elif config_path is not None:
            if os.path.isabs(config_path):
                config = yaml.safe_load(config_path)
            else:
                caller_file = inspect.stack()[1][0].f_code.co_filename
                config_path = os.path.join(os.path.split(caller_file)[0], config_path)
                config = yaml.safe_load(open(config_path))
        self._config = config
        self._medium = self._init_medium(space)
        self._medium.activate()

    def persist(self, k, v):
        self._medium.persist(k, v)

    def cache(self, k, v):
        self._medium.cache(k, v)

    def flush(self):
        self._medium.flush()

    def _init_medium(self, space):
        param, medium = self._config["param"], self._config["medium"]
        if medium == "mysql":
            medium = MysqlMedium(space, param)
        else:
            raise Exception("Medium type %s not supported. " % medium)
        return medium
