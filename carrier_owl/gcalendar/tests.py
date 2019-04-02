import datetime
import unittest
from unittest import mock

from django.test import TestCase
import pytz

from carrier_owl.factories import UserFactory, UserSocialAuthFactory
from gcalendar.api import GoogleCalendarAPI


class GoogleCalendarDateTimeTestCase(unittest.TestCase):

    def setUp(self):
        self.dt_jan_1 = datetime.datetime(2019, 1, 1)

    def test_gcalendar_timestamp(self):
        self.assertEqual(GoogleCalendarAPI.gcalendar_timestamp(self.dt_jan_1), '2019-01-01T00:00:00')

    def test_gcalendar_datetime(self):
        self.assertEqual(
            GoogleCalendarAPI.gcalendar_datetime(self.dt_jan_1),
            {
                'dateTime': '2019-01-01T00:00:00',
                'timeZone': 'America/Los_Angeles',
            }
        )


class GoogleCalendarAPIAccessTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = UserFactory(is_superuser=True)

    def test_get_only_superuser(self):
        self.assertEqual(GoogleCalendarAPI.get_only_superuser(), self.superuser)

    @mock.patch('social_django.models.UserSocialAuth.get_access_token')
    def test_get_access_token_from_superuser(self, mock_get_access_token):
        access_token = UserSocialAuthFactory.extra_data['access_token']
        mock_get_access_token.return_value = access_token

        self.assertEqual(GoogleCalendarAPI.get_access_token_from_superuser(), access_token)


class GoogleCalendarAPITestCase(unittest.TestCase):

    def setUp(self):
        self.dt_jan_5 = datetime.datetime(2019, 1, 5, 18, 30).astimezone(pytz.timezone('America/Los_Angeles'))
        self.event = {
            'kind': 'calendar#event',
            'etag': '"1234"',
            'id': '1234_20190101T000000Z',
            'status': 'confirmed',
            'htmlLink': 'https://www.google.com/calendar/event?eid=abc123',
            'created': '2019-01-01T00:00:00.000Z',
            'updated': '2019-01-01T00:00:00.000Z',
            'summary': 'Event Title',
            'creator': {'email': 'jsmith@gmail.com', 'displayName': 'John Smith', 'self': True},
            'organizer': {'email': 'jsmith@gmail.com', 'displayName': 'John Smith', 'self': True},
            'start': {'dateTime': '2019-01-05T18:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'end': {'dateTime': '2019-01-05T19:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'recurringEventId': 'abc123',
            'originalStartTime': {'dateTime': '2019-01-05T18:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'iCalUID': 'abc123@google.com',
            'sequence': 0,
            'attendees': [],
            'reminders': {'useDefault': False},
        }
        with mock.patch(
            'gcalendar.api.GoogleCalendarAPI.get_access_token_from_superuser',
            return_value=UserSocialAuthFactory.extra_data['access_token']
        ):
            self.api = GoogleCalendarAPI()

    @mock.patch('gcalendar.api.discovery.HttpRequest.execute')
    def test_get_events_at_time(self, mock_execute):
        mock_execute.return_value = {'items': [self.event]}

        self.assertEqual(self.api.get_events_at_time(dt=self.dt_jan_5), [self.event])

    @mock.patch('gcalendar.api.discovery.HttpRequest.execute')
    def test_has_event_at_time(self, mock_execute):
        mock_execute.return_value = {'items': [self.event]}

        self.assertTrue(self.api.has_event_at_time(dt=self.dt_jan_5))

    @mock.patch('gcalendar.api.discovery.HttpRequest.execute')
    def test_create_event(self, mock_execute):
        start = self.dt_jan_5.replace(hour=18, minute=0)
        end = self.dt_jan_5.replace(hour=19, minute=0)

        self.api.create_event(
            summary='Event Title',
            start=start,
            end=end,
            description='Event Description',
            location='Location',
            attendees=['jsmith@gmail.com']
        )
        mock_execute.assert_called_once()
