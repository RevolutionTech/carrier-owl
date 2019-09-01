from django.test import TestCase

from event.tests.factories import EventFactory


class EventModelsTestCase(TestCase):
    def test_event_str(self):
        event = EventFactory()
        self.assertEqual(event.summary, str(event))
