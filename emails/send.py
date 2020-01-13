from django.conf import settings
from django.core.mail import send_mail

from emails.message import generate_customized_message


def send_emails(event):
    for guest in event.guests.all():
        send_mail(
            event.subject,
            generate_customized_message(event.message, guest),
            settings.DEFAULT_FROM_EMAIL,
            [guest.email],
            fail_silently=False,
        )
