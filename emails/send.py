from django.conf import settings
from django.core.mail import send_mail

from emails.message import generate_customized_message


def send_emails(event):
    for attendee in event.attendees.all():
        send_mail(
            event.summary,
            generate_customized_message(event, attendee),
            settings.DEFAULT_FROM_EMAIL,
            [attendee.email],
            fail_silently=False,
        )
