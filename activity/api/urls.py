from django.urls import path

from .views import BlockRetravie

urlpatterns = [path("<int:pk>/", BlockRetravie.as_view())]
