from django.conf import settings

from event.utils import calculate_next_weekday, event_midpoint
from gcalendar.api import GoogleCalendarAPI


def create_next_weekly_event():
    next_event_day = calculate_next_weekday(settings.EVENT_WEEKDAY)
    next_event_start = next_event_day.replace(hour=settings.EVENT_START_HOUR, minute=settings.EVENT_START_MINUTE)
    next_event_end = next_event_day.replace(hour=settings.EVENT_END_HOUR, minute=settings.EVENT_END_MINUTE)
    next_event_midpoint = event_midpoint(next_event_start, next_event_end)

    gcal_api = GoogleCalendarAPI()
    if not gcal_api.has_event_at_time(next_event_midpoint):
        gcal_api.create_event(
            summary=settings.EVENT_SUMMARY,
            start=next_event_start,
            end=next_event_end,
            description=settings.EVENT_DESCRIPTION,
            location=settings.EVENT_LOCATION,
            attendees=settings.EVENT_ATTENDEES
        )
