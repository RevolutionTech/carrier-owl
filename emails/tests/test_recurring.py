from unittest import mock

from django.test import TestCase

from emails.recurring import send_weekly_invites
from event.tests.factories import EventFactory


@mock.patch("emails.recurring.send_emails")
@mock.patch("emails.recurring.GoogleCalendarAPI")
class TestSendWeeklyInvites(TestCase):
    def test_send_weekly_invites(self, mock_gcal_api, mock_send_emails):
        mock_gcal_api.return_value = mock.Mock(
            has_event_during_time=lambda start, end: True
        )

        event = EventFactory()

        send_weekly_invites()
        mock_send_emails.assert_called_once_with(event)

    def test_weekly_invites_do_not_send_if_event_does_not_exist(
        self, mock_gcal_api, mock_send_emails
    ):
        mock_gcal_api.return_value = mock.Mock(
            has_event_during_time=lambda start, end: False
        )

        EventFactory()

        send_weekly_invites()
        mock_send_emails.assert_not_called()
