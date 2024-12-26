from utilities.response import res200, res400, res500
from utilities.tinify_client import tinify_client
from conf.config import config
from typing import Union
import webview
import time


class SettingAPI:
    name = "setting"

    def get(self, params: Union[dict, None] = None):
        return res200(dict(config))

    def put(self, playload: dict):
        for key, value in playload.items():
            if key in config:
                config.save(key, value)
            if key == "tinify.tinify_key":
                tinify_client.update_key(value)
            if key.startswith("edge_optimization"):
                config.save(key, value)
            if key.startswith("api_server"):
                config.save(key, value)
        return res200(dict(config))

    def update_window_setting(self, payload):
        window = webview.windows[0]
        time.sleep(0.1)  # If we don't sleep, the window will get frozen. Have no idea.
        pin_window = payload.get("pin_window")
        if pin_window is not None:
            window.on_top = pin_window
            config.save("window.on_top", pin_window)
        return res200()
