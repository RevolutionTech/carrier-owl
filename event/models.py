import calendar

from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):

    EVENT_WEEKDAY_CHOICES = (
        (weekday, calendar.day_name[weekday]) for weekday in range(7)
    )

    subject = models.TextField()
    message = models.TextField()
    weekday = models.PositiveSmallIntegerField(choices=EVENT_WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    guests = models.ManyToManyField(User, limit_choices_to={"is_superuser": False})

    def __str__(self):
        return self.subject
