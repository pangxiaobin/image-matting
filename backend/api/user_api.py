from utilities.response import res200, res400, res500
from conf.config import config
from typing import Union
import json


class SettingAPI:
    name = "setting"

    def get(self, params: Union[dict, None] = None):
        return res200(dict(config))

    def put(self, playload: dict):
        for key, value in playload.items():
            if key in config:
                config.save(key, value)
        return res200(dict(config))
