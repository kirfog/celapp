import pytest

from src.celery.celery import config_dict

pytest_plugins = ("celery.contrib.pytest",)

config_dict["broker_url"] = "redis://localhost:6379/10"
config_dict["result_backend"] = "redis://localhost:6379/10"
config_dict["redbeat_redis_url"] = "redis://localhost:6379/11"


@pytest.fixture(scope="session")
def celery_config():
    return config_dict


@pytest.fixture(autouse=True)
def clean_redis():
    import redis

    broker_db = config_dict["broker_url"].split("/")[-1]
    redbeat_db = config_dict["redbeat_redis_url"].split("/")[-1]

    for db in [broker_db, redbeat_db]:
        r = redis.Redis(db=int(db))
        r.flushdb()
