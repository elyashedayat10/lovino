from django.urls import path

from .views import ProfileApiView

urlpatterns = [
    path('', ProfileApiView.as_view()),
    # path('verify/', VerifyApiView.as_view())
]


