from apiclient import discovery
from django.contrib.auth.models import User
from oauth2client.client import AccessTokenCredentials
from social_django.utils import load_strategy


class GoogleCalendarAPI:

    CALENDAR_ID_PRIMARY = "primary"

    @staticmethod
    def gcalendar_timestamp(dt):
        return dt.isoformat()

    @staticmethod
    def get_only_superuser():
        return User.objects.get(is_superuser=True)

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

    def get_events_during_time(self, start, end, max_results=None):
        results = self.events_api.list(
            calendarId=self.CALENDAR_ID_PRIMARY,
            orderBy="startTime",
            timeMin=self.gcalendar_timestamp(start),
            singleEvents=True,
            maxResults=max_results,
            timeMax=self.gcalendar_timestamp(end),
        ).execute()
        events = results.get("items", [])
        return events

    def has_event_during_time(self, start, end):
        return bool(self.get_events_during_time(start, end, max_results=1))
