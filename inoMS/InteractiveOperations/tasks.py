# for use celery
from inoMS.celery import app


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 4, 'countdown': 5})
def my_task(self):
    pass
