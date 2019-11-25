from unittest import mock

from django.test import TestCase

from emails.recurring import send_weekly_invites
from event.tests.factories import EventFactory


class TestSendWeeklyInvites(TestCase):
    @mock.patch("emails.recurring.send_emails")
    def test_send_weekly_invites(self, mock_send_emails):
        event = EventFactory()

        send_weekly_invites()
        mock_send_emails.assert_called_once_with(event)
