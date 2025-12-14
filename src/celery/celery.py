import yaml

from celery import Celery
from src.celery.rb import load_redbeat_tasks

"""
celery -A celapp worker
# celery -A celapp beat -S redbeat.RedBeatScheduler
celery -A celapp beat
"""

app = Celery("celery")

config_dict = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/0",
    "timezone": "Europe/London",
    "enable_utc": True,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "beat_scheduler": "redbeat.RedBeatScheduler",
    "redbeat_redis_url": "redis://localhost:6379/1",
    "redbeat_lock_key": None,
}


app.conf.update(config_dict)
app.autodiscover_tasks(["src.celery"])


with open("src/celery/redbeat.yml", "r") as f:
    tasks_config = yaml.safe_load(f) or {}

load_redbeat_tasks(app, tasks_config)
