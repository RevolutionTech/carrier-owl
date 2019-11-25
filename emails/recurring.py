from django.conf import settings

from emails.send import send_emails
from event.models import Event


def send_weekly_invites():
    if settings.EXPERIMENT_SEND_ATTENDEES_INVITATION_EMAIL:
        for event in Event.objects.all():
            send_emails(event)
