from typing import Literal

from pydantic import BaseSettings, BaseModel

RESERVED_ENVS = ["Config"]

class Settings(BaseSettings):
    _fallback_settings = {}

    class Config:
        env_nested_delimiter = '__'

    need_debug: bool = False
    need_reload: bool = False
    log_level: Literal["TRACE", "DEBUG", "INFO",
                       "WARNING", "ERROR", "CRITICAL"] = "TRACE"

    host: str = "0.0.0.0"
    port: int = 5000

    SQLALCHEMY_DATABASES: dict = {
        "default": {
            "uri": "mysql+pymysql://mysql:mysql123@127.0.0.1:3306/test?charset=utf8",
            "pool_size": 2
        }
    }

    def __init__(self):
        super().__init__()
        self._update_env_settings()

    def _update_env_settings(self):
        data = {}
        for attr, value in self.dict().items():
            data[attr] = value
        self._fallback_settings.update(data)
        print(self._fallback_settings)

    def __getitem__(self, key):
        if key not in self._fallback_settings:
            raise KeyError(
                f'missing config[{key}], typo or forgot to populate?')
        return self._fallback_settings[key]

    def get(self, key, default=None):
        return self._fallback_settings.get(key, default)


settings = Settings()
