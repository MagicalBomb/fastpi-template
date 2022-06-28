from typing import Literal

from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    class Config:
        env_nested_delimiter = '__'

    need_debug: bool = False
    need_reload: bool = False
    log_level: Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "TRACE"

    host: str = "0.0.0.0"
    port: int = 5000


settings = Settings()
