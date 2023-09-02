from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """Base config"""

    environment: str
    database_uri: PostgresDsn

    class Config:
        """Config class"""

        env_file = ".env"
        _env_file_encoding = "utf-8"


class ProductionSettings(BaseConfig):
    """production settings"""

    pass


class DevelopmentSettings(BaseConfig):
    """development settings"""

    pass


class TestSettings(BaseConfig):
    """test settings"""

    pass


@lru_cache
def get_settings():
    """Get settings"""
    configs = {
        "production": ProductionSettings,
        "development": DevelopmentSettings,
        "testing": TestSettings,
    }
    environment = BaseConfig().environment

    return configs[environment]()


settings = get_settings()
