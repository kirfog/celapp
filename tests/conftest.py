import pytest

from src.celery.celery import config_dict

pytest_plugins = ("celery.contrib.pytest",)

config_dict["broker_url"] = "redis://localhost:6379/10"
config_dict["result_backend"] = "redis://localhost:6379/10"
config_dict["beat_scheduler"] = "redis://localhost:6379/11"


@pytest.fixture(scope="session")
def celery_config():
    return config_dict
