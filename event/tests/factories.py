import datetime

import factory

from event.models import Event


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    summary = "Example title"
    weekday = 2  # Wednesday
    start_time = datetime.time(hour=14, minute=0)  # 2pm
    end_time = datetime.time(hour=15, minute=0)  # 3pm
