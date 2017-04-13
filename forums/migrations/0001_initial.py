# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-13 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import misago.users.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('misago_users', '0009_auto_20170413_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='misago_users.User')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('misago_users.user',),
            managers=[
                ('objects', misago.users.models.user.UserManager()),
            ],
        ),
    ]
