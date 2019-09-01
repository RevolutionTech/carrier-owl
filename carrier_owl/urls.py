from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path


urlpatterns = [
    url("", include(("social_django.urls", "social"))),
    path("admin/", admin.site.urls),
]
