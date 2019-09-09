import datetime

import pytz
from django.conf import settings
from django.utils import timezone


def number_days_until_next_weekday(dt, weekday):
    return (weekday - dt.weekday()) % 7


def calculate_next_weekday(weekday):
    now = timezone.now().astimezone(pytz.timezone(settings.GCALENDAR_EVENT_TIMEZONE))
    next_weekday_this_time = now + datetime.timedelta(
        days=number_days_until_next_weekday(now, weekday)
    )
    next_weekday_this_hour = next_weekday_this_time.replace(
        minute=0, second=0, microsecond=0
    )
    return next_weekday_this_hour
