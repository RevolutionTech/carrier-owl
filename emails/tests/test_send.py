from django.conf import settings
from django.core import mail
from django.test import TestCase

from carrier_owl.factories import UserFactory
from emails.send import send_emails
from event.tests.factories import EventFactory


class TestSendEmails(TestCase):
    def test_send_emails(self):
        users = UserFactory.create_batch(2)
        event = EventFactory()
        event.guests.set(users)

        send_emails(event)
        self.assertEqual(len(mail.outbox), len(users))

        for user, email in zip(users, mail.outbox):
            self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
            self.assertEqual(email.to, [user.email])
            self.assertEqual(email.subject, event.subject)
            self.assertEqual(
                email.body, f"Hey {user.first_name},\n\nExample message",
            )
