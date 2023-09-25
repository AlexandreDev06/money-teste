from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """Base config"""

    environment: str
    db_uri: str
    lawtech_api: str
    redis_url: str
    volpe_url: str
    volpe_api_key: str
    capmonster_api_key: str
    zap_sign_token: str

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
