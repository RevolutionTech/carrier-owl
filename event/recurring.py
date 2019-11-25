from django.conf import settings

from emails.recurring import send_weekly_invites
from event.models import Event
from event.utils import calculate_next_weekday
from gcalendar.api import GoogleCalendarAPI


def create_next_weekly_events():
    for event in Event.objects.all():
        next_event_day = calculate_next_weekday(event.weekday)
        next_event_start = next_event_day.replace(
            hour=event.start_time.hour, minute=event.start_time.minute
        )
        next_event_end = next_event_day.replace(
            hour=event.end_time.hour, minute=event.end_time.minute
        )

        gcal_api = GoogleCalendarAPI()
        if not gcal_api.has_event_during_time(next_event_start, next_event_end):
            attendee_emails = []
            if settings.EXPERIMENT_ADD_ATTENDEES_TO_EVENT:
                attendee_emails = [
                    email for email in event.attendees.values_list("email", flat=True)
                ]

            gcal_api.create_event(
                summary=event.summary,
                start=next_event_start,
                end=next_event_end,
                description=event.description,
                location=event.location,
                attendees=attendee_emails,
            )


def create_events_and_notify_attendees():
    create_next_weekly_events()
    send_weekly_invites()
