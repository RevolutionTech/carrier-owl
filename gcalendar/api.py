import datetime

from django.conf import settings
from django.contrib.auth.models import User

from apiclient import discovery
from oauth2client.client import AccessTokenCredentials
from social_django.utils import load_strategy


class GoogleCalendarAPI(object):

    CALENDAR_ID_PRIMARY = "primary"

    @staticmethod
    def gcalendar_timestamp(dt):
        return dt.isoformat()

    @staticmethod
    def get_only_superuser():
        return User.objects.get(is_superuser=True)

    @classmethod
    def gcalendar_datetime(cls, dt):
        return {
            "dateTime": cls.gcalendar_timestamp(dt),
            "timeZone": settings.GCALENDAR_EVENT_TIMEZONE,
        }

    @classmethod
    def get_access_token_from_superuser(cls):
        strategy = load_strategy()
        user = cls.get_only_superuser()
        social = user.social_auth.get()
        return social.get_access_token(strategy)

    def __init__(self):
        access_token = self.get_access_token_from_superuser()
        credentials = AccessTokenCredentials(access_token, "python-requests")
        service = discovery.build("calendar", "v3", credentials=credentials)
        self.events_api = service.events()

    def get_events_at_time(self, dt, max_results=None):
        results = self.events_api.list(
            calendarId=self.CALENDAR_ID_PRIMARY,
            orderBy="startTime",
            timeMin=self.gcalendar_timestamp(dt),
            singleEvents=True,
            maxResults=max_results,
            timeMax=self.gcalendar_timestamp(dt + datetime.timedelta(seconds=1)),
        ).execute()
        events = results.get("items", [])
        return events

    def has_event_at_time(self, dt):
        return bool(self.get_events_at_time(dt, max_results=1))

    def create_event(self, summary, start, end, description, location, attendees):
        return self.events_api.insert(
            calendarId=self.CALENDAR_ID_PRIMARY,
            body={
                "summary": summary,
                "start": self.gcalendar_datetime(start),
                "end": self.gcalendar_datetime(end),
                "description": description,
                "location": location,
                "attendees": [{"email": email} for email in attendees],
            },
            sendUpdates="all",
        ).execute()
