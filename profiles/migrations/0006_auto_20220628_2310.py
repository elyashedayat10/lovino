# Generated by Django 3.2.13 on 2022-06-28 18:40

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20220627_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]