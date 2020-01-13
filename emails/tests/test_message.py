from django.test import TestCase

from carrier_owl.factories import UserFactory
from emails.message import generate_customized_message


class TestGenerateCustomizedMessage(TestCase):
    def test_generate_customized_message(self):
        user = UserFactory(first_name="John")
        message = "Hope you can make it!"

        self.assertEqual(
            generate_customized_message(message, user),
            f"Hey John,\n\nHope you can make it!",
        )
