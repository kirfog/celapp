import pytest

pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379/10',
        'result_backend': 'redis://localhost:6379/10',
        'redbeat_redis_url': 'redis://localhost:6379/11',
        'redbeat_lock_key': None,
    }
