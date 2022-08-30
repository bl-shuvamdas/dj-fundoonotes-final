from smtplib import SMTPException
from typing import List

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from django.utils.timezone import timedelta

from utils import JWT


class Email:
    @staticmethod
    def send(subject: str, body: str, to: List[str]):
        try:
            send_mail(
                subject=subject,
                message=body,
                recipient_list=to,
                from_email=None
            )
        except SMTPException as e:
            raise Exception(str(e))

    @classmethod
    def verify_user(cls, email: str):
        subject = 'Register your self'

        token = JWT.encode(payload={'email': email}, exp=timedelta(minutes=30))
        url = reverse('auth:verify', kwargs={'token': token})
        body = 'Hii %s, Use this link to verify yourself,\n' % email
        body += '%s%s' % (settings.BASE_URL, url)
        cls.send(subject=subject, body=body, to=[email])
