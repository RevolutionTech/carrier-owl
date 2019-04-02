import datetime
from unittest import mock

from django.test import SimpleTestCase, override_settings
import pytz

from event.utils import calculate_next_weekday, event_midpoint, number_days_until_next_weekday


class EventUtilsTestCase(SimpleTestCase):

    WEEKDAY_MONDAY = 0
    WEEKDAY_THURSDAY = 3

    @staticmethod
    def dt_jan_2019(day):
        return datetime.datetime(2019, 1, day).astimezone(pytz.timezone('UTC'))

    def test_number_days_until_next_weekday(self):
        dt_jan_1 = self.dt_jan_2019(1)  # Jan 1st was a Tuesday

        self.assertEqual(number_days_until_next_weekday(dt=dt_jan_1, weekday=self.WEEKDAY_THURSDAY), 2)
        self.assertEqual(number_days_until_next_weekday(dt=dt_jan_1, weekday=self.WEEKDAY_MONDAY), 6)

    @mock.patch('event.utils.timezone.now')
    @override_settings(GCALENDAR_EVENT_TIMEZONE='UTC')
    def test_calculate_next_weekday(self, mock_timezone_now):
        mock_timezone_now.return_value = self.dt_jan_2019(1)

        self.assertEqual(calculate_next_weekday(weekday=self.WEEKDAY_THURSDAY), self.dt_jan_2019(3))

    def test_event_midpoint(self):
        self.assertEqual(event_midpoint(start=self.dt_jan_2019(1), end=self.dt_jan_2019(3)), self.dt_jan_2019(2))
