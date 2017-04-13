from __future__ import unicode_literals

from django.db import models
from misago.users.models.user import User, UserManager

# Create your models here.
class User(User):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    objects = UserManager()
