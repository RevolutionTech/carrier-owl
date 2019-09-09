import datetime
from unittest import mock

from django.test import TestCase

from carrier_owl.factories import UserFactory
from event.recurring import create_next_weekly_events
from event.tests.factories import EventFactory
from event.utils import calculate_next_weekday


class EventRecurringTestCase(TestCase):

    EVENT_WEEKDAY = 2  # Wednesday
    EVENT_START_TIME = datetime.time(hour=14, minute=0)  # 2pm
    EVENT_END_TIME = datetime.time(hour=15, minute=0)  # 3pm
    EVENT_SUMMARY = "Afternoon Tea"
    EVENT_DESCRIPTION = "Drink some tea with us!"
    EVENT_LOCATION = "San Francisco, CA"
    EVENT_ATTENDEES = ["jsmith@example.com", "mdoe@example.com"]

    @mock.patch("event.recurring.GoogleCalendarAPI")
    def test_create_next_weekly_events(self, mock_gcal_api):
        create_event_mock = mock.Mock()
        mock_gcal_api.return_value = mock.Mock(
            has_event_during_time=lambda start, end: False,
            create_event=create_event_mock,
        )

        event = EventFactory(
            weekday=self.EVENT_WEEKDAY,
            start_time=self.EVENT_START_TIME,
            end_time=self.EVENT_END_TIME,
            summary=self.EVENT_SUMMARY,
            description=self.EVENT_DESCRIPTION,
            location=self.EVENT_LOCATION,
        )
        event.attendees.set(
            [UserFactory(email=email) for email in self.EVENT_ATTENDEES]
        )
        next_event_day = calculate_next_weekday(self.EVENT_WEEKDAY)

        create_next_weekly_events()
        create_event_mock.assert_called_once_with(
            summary=self.EVENT_SUMMARY,
            start=next_event_day.replace(hour=14, minute=0),
            end=next_event_day.replace(hour=15, minute=0),
            description=self.EVENT_DESCRIPTION,
            location=self.EVENT_LOCATION,
            attendees=self.EVENT_ATTENDEES,
        )

    @mock.patch("event.recurring.GoogleCalendarAPI")
    def test_create_next_weekly_events_skips_with_existing_event(self, mock_gcal_api):
        create_event_mock = mock.Mock()
        mock_gcal_api.return_value = mock.Mock(
            has_event_during_time=lambda start, end: True,
            create_event=create_event_mock,
        )

        create_next_weekly_events()
        create_event_mock.assert_not_called()
