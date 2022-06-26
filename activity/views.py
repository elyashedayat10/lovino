from django.shortcuts import render
from django.views.generic import DetailView, ListView

from utils.mixins import AdminUserMixin

from .models import ReportedUser


# Create your views here.
class ReportedUserList(AdminUserMixin, ListView):
    model = ReportedUser
    template_name = ""
