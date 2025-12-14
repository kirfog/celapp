from celery import shared_task


@shared_task
def mul(x, y):
    return x * y


@shared_task
def su(x, y):
    return x + y


@shared_task(ignore_result=False)
def task1():
    res = {"task": "task1"}
    return res


@shared_task(ignore_result=False)
def task2():
    res = {"task": "task2"}
    return res


@shared_task(ignore_result=False)
def task3(a, b):
    res = {"task": "task3", "result": a + b}
    return res


@shared_task(ignore_result=False)
def task4(a, b):
    res = {"task": "task4", "result": a * b}
    return res
