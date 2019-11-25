from django.test import TestCase

from carrier_owl.factories import UserFactory
from emails.message import generate_customized_message
from event.tests.factories import EventFactory


class TestGenerateCustomizedMessage(TestCase):
    def test_generate_customized_message(self):
        user = UserFactory(first_name="John")
        event = EventFactory(description="Hope you can make it!")

        self.assertEqual(
            generate_customized_message(event, user),
            f"Hey John,\n\nHope you can make it!",
        )
