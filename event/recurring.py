from event.models import Event
from event.utils import calculate_next_weekday, event_midpoint
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
        next_event_midpoint = event_midpoint(next_event_start, next_event_end)

        gcal_api = GoogleCalendarAPI()
        if not gcal_api.has_event_at_time(next_event_midpoint):
            gcal_api.create_event(
                summary=event.summary,
                start=next_event_start,
                end=next_event_end,
                description=event.description,
                location=event.location,
                attendees=[
                    email for email in event.attendees.values_list("email", flat=True)
                ],
            )
