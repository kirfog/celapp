from redbeat import RedBeatSchedulerEntry as Entry

from celery.schedules import crontab, schedule


def parse_schedule(cfg):
    if isinstance(cfg, (int, float)):
        return schedule(float(cfg))
    elif isinstance(cfg, dict):
        if any(
            k in cfg
            for k in {"minute", "hour", "day_of_week", "day_of_month", "month_of_year"}
        ):
            return crontab(**cfg)
        else:
            raise ValueError(f"Unrecognized schedule dict: {cfg}")
    else:
        raise TypeError(f"Unsupported schedule type: {type(cfg)}")


def load_redbeat_tasks(app, tasks_config):
    for name, config in tasks_config.items():
        entry = Entry(
            name=name,
            task=config["task"],
            schedule=parse_schedule(config["schedule"]),
            args=config["args"],
            kwargs=config["kwargs"],
            options=config["options"],
            app=app,
        )
        entry.enabled = config["enabled"]
        entry.save()


def list_redbeat_tasks(app, rd):
    tasks = []
    for key in rd.scan_iter(match="redbeat:*"):
        if rd.type(key) != b"hash":
            continue
        try:
            name = key.decode().replace("redbeat:", "")
            entry = Entry.from_key(f"redbeat:{name}", app=app)
            tasks.append(
                {
                    "name": entry.name,
                    "task": entry.task,
                    "schedule": entry.schedule,
                    "args": list(entry.args or []),
                    "kwargs": dict(entry.kwargs or {}),
                    "options": dict(entry.options or {}),
                    "enabled": bool(entry.enabled),
                    "run_immediately": bool(getattr(entry, "run_immediately", False)),
                    "last_run_at": entry.last_run_at,
                    "total_run_count": entry.total_run_count,
                }
            )
        except Exception as e:
            print(f"Failed to load RedBeat task {key}: {e}")
            continue
    return sorted(tasks, key=lambda x: x["name"])


def save_task(app, task_name, task, schedule, args=None, kwargs=None, options=None):
    entry = Entry(
        name=task_name,
        task=task,
        schedule=schedule,
        args=args or [],
        kwargs=kwargs or {},
        options=options or {},
        app=app,
    )
    entry.save()


def delete_task(app, task_name):
    try:
        entry = Entry.from_key(f"redbeat:{task_name}", app=app)
        entry.delete()
        print(f"Task '{task_name}' deleted.")
    except KeyError:
        print(f"Task '{task_name}' not found.")


if __name__ == "__main__":
    import redis
    from celapp.celery import app
    rd = redis.Redis(host="localhost", port=6379, db=2)
    print(list_redbeat_tasks(app, rd))
