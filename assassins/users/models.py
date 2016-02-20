from __future__ import unicode_literals

from django.db import models

# Default user gives us some fields for free
#  username, first_name, last_name, email, is_staff, is_active, date_joined
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	profile_picture_url = models.CharField(
		max_length=200,
		blank=False,
	)
	major = models.CharField(max_length=50)
