from django.urls import path

from .views import AuthApiView, VerifyApiView, LogoutApiView

urlpatterns = [
    path('auth/', AuthApiView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('logout/', LogoutApiView.as_view())
]
