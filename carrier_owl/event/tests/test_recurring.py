from unittest import mock

from django.test import SimpleTestCase, override_settings

from event.recurring import create_next_weekly_event
from event.utils import calculate_next_weekday


class EventRecurringTestCase(SimpleTestCase):

    EVENT_WEEKDAY = 2  # Wednesday
    EVENT_SUMMARY = 'Afternoon Tea'
    EVENT_DESCRIPTION = 'Drink some tea with us!'
    EVENT_LOCATION = 'San Francisco, CA'
    EVENT_ATTENDEES = ['jsmith@example.com', 'mdoe@example.com']

    @mock.patch('event.recurring.GoogleCalendarAPI')
    @override_settings(
        EVENT_WEEKDAY=2, EVENT_START_HOUR=14, EVENT_START_MINUTE=0, EVENT_END_HOUR=15, EVENT_END_MINUTE=0,
        EVENT_SUMMARY=EVENT_SUMMARY, EVENT_DESCRIPTION=EVENT_DESCRIPTION, EVENT_LOCATION=EVENT_LOCATION,
        EVENT_ATTENDEES=EVENT_ATTENDEES
    )
    def test_create_next_weekly_event(self, mock_gcal_api):
        create_event_mock = mock.Mock()
        mock_gcal_api.return_value = mock.Mock(has_event_at_time=lambda _: False, create_event=create_event_mock)

        next_event_day = calculate_next_weekday(self.EVENT_WEEKDAY)

        create_next_weekly_event()
        create_event_mock.assert_called_once_with(
            summary=self.EVENT_SUMMARY,
            start=next_event_day.replace(hour=14, minute=0),
            end=next_event_day.replace(hour=15, minute=0),
            description=self.EVENT_DESCRIPTION,
            location=self.EVENT_LOCATION,
            attendees=self.EVENT_ATTENDEES
        )

    @mock.patch('event.recurring.GoogleCalendarAPI')
    def test_create_next_weekly_event_skips_with_existing_event(self, mock_gcal_api):
        create_event_mock = mock.Mock()
        mock_gcal_api.return_value = mock.Mock(has_event_at_time=lambda _: True, create_event=create_event_mock)

        create_next_weekly_event()
        create_event_mock.assert_not_called()
