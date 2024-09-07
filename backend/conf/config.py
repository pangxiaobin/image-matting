# config.py
import json
import threading
from pathlib import Path
from threading import Lock
from collections.abc import Mapping

DEFAULT_CONFIG = {
    "language": "zh-CN",
    "save_dir": "./data",
    "theme": "light",
    "window": {
        "width": 1037,
        "height": 800,
        "x": 249,
        "y": 23,
        "fullscreen": False,
        "on_top": False,
    },
    "tinify": {"tinify_key": "", "preserve": [], "compression_count": 0},
}


class Config(Mapping):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.config_path = Path(__file__).parent.parent / "config.json"
        self._dirty = False
        self._save_interval = 5
        self._save_timer = None

        if not self.config_path.is_file():
            with open(self.config_path, "w", encoding="utf8") as config_file:
                json.dump(DEFAULT_CONFIG, config_file)

        self.config = DEFAULT_CONFIG
        with open(self.config_path, "r") as config_file:
            self.config.update(json.load(config_file))

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def save(self, key, value):
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._dirty = True

        if self._save_timer is None:
            self._start_save_timer()

    def _save_to_file(self):
        with open(self.config_path, "w", encoding="utf8") as config_file:
            json.dump(self.config, config_file, indent=4, ensure_ascii=False)
        self._dirty = False

    def _start_save_timer(self):
        self._save_timer = threading.Timer(self._save_interval, self._periodic_save)
        self._save_timer.start()

    def _periodic_save(self):
        if self._dirty:
            self._save_to_file()
        self._save_timer = None

    def close(self):
        if self._save_timer is not None:
            self._save_timer.cancel()
            self._save_timer = None
        if self._dirty:
            self._save_to_file()

    @property
    def data_path(self):
        return self.get("data_path", "./data")

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)


config = Config()
