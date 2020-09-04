import datetime

import factory

from event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    subject = "Example title"
    message = "Example message"
    weekday = 2  # Wednesday
    start_time = datetime.time(hour=14, minute=0)  # 2pm
    end_time = datetime.time(hour=15, minute=0)  # 3pm
