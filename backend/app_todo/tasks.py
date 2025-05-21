from celery import shared_task
from time import sleep
from mail_templated import EmailMessage
from django_celery_beat.models import PeriodicTask


@shared_task
def send_email():
    sleep(5)
    email_object = EmailMessage(
        "email/test.tpl",
        {"name": "the admin1"},
        "from@example.com",
        to=["to@example.com"],
    )
    email_object.send()


@shared_task
def delete_done_tasks():
    tasks = PeriodicTask.objects.all()
    important_tasks = ['celery.backend_cleanup', 'delete done tasks']
    for task in tasks:
        if not task.name in important_tasks:
            if task.last_run_at:
                task.delete()