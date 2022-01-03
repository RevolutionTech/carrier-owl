from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("social_django.urls", "social"))),
    path("admin/", admin.site.urls),
]
