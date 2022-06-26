import datetime

import jdatetime
from django.conf import settings
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_jalali.db import models as jmodels

user = settings.AUTH_USER_MODEL
from accounts.models import User

# Create your models here.


class ActiveProfileManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(is_activae=True, **kwargs)


class Profile(TimeStampedModel):
    GENDER = (
        ("MALE", "مرد"),
        ("FEMALE", "زن"),
    )
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_name = models.CharField(
        blank=True,
        max_length=125,
        unique=True,
    )
    province = models.CharField(
        blank=True,
        max_length=125,
    )
    city = models.CharField(
        blank=True,
        max_length=125,
    )
    first_name = models.CharField(
        blank=True,
        max_length=125,
    )
    last_name = models.CharField(
        blank=True,
        max_length=125,
    )
    bio = models.CharField(
        blank=True,
        max_length=500,
    )
    gender = models.CharField(
        blank=True,
        max_length=10,
        choices=GENDER,
    )
    birthdate = jmodels.jDateField(
        blank=True,
    )
    age = models.PositiveIntegerField(
        blank=True,
        validators=[MinValueValidator, MaxValueValidator],
    )
    is_active = models.BooleanField(default=True)

    objects = ActiveProfileManager()

    def save(self, **kwargs):
        if self.birthdate:
            user_age = jdatetime.date.today() - self.birthdate
            self.age = user_age.year
            return super(Profile, self).save(**kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to="")
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )

    def clean(self):
        user_obj = User.objects.get(id=self.user.id)
        if user_obj.images.count() >= 5:
            raise ValidationError("max image for each user is five")
