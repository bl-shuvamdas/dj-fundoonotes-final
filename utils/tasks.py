from celery import shared_task, exceptions
from os import getenv

from .email_service import Email


@shared_task
def send_verify_email(email):
    try:
        Email.verify_user(email)
        return 'successfully sent'
    except exceptions.CeleryError as e:
        raise e
