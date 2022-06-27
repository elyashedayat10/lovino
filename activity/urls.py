from django.urls import include, path

from activity.api.urls import urlpatterns

urlpatterns = [path("api/", include(urlpatterns))]
