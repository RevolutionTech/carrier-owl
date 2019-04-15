from django.contrib.auth.models import User
from social_django.models import UserSocialAuth

import factory


class UserFactory(factory.DjangoModelFactory):

    _PASSWORD = 'abc123'

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda user: "{username}@gmail.com".format(username=user.username))
    social_auth = factory.RelatedFactory('carrier_owl.factories.UserSocialAuthFactory', 'user')


class UserSocialAuthFactory(factory.DjangoModelFactory):

    class Meta:
        model = UserSocialAuth

    user = factory.SubFactory(UserFactory)
    uid = factory.LazyAttribute(lambda usa: usa.user.email)
    extra_data = {
        "auth_time": 1546300800,
        "expires": 3600,
        "token_type": "Bearer",
        "access_token": "ya29.abc123",
        "refresh_token": "1/abc123",
    }
