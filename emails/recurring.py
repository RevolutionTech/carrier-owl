from emails.send import send_emails
from event.models import Event
from event.utils import calculate_next_weekday
from gcalendar.api import GoogleCalendarAPI


def send_weekly_invites():
    for event in Event.objects.all():
        next_event_day = calculate_next_weekday(event.weekday)
        next_event_start = next_event_day.replace(
            hour=event.start_time.hour, minute=event.start_time.minute
        )
        next_event_end = next_event_day.replace(
            hour=event.end_time.hour, minute=event.end_time.minute
        )

        gcal_api = GoogleCalendarAPI()
        if gcal_api.has_event_during_time(next_event_start, next_event_end):
            send_emails(event)
