from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Game(models.Model):
	name = models.CharField(
		max_length = 20,
		default = 'Game',
		blank = False,
	)
	description = models.TextField(
		null = True,
	)
	max_num_players = models.PositiveIntegerField()
	start_date = models.DateTimeField(
		blank = False,
	)
	round_length = models.DurationField(
		blank = False,
	)

	PLAYER_APPROVAL_CHOICES = (
		(0, 'Admin'),
		(1, 'All'),
	)
	approval_preference = models.PositiveIntegerField(
		default = 0,
		choices = PLAYER_APPROVAL_CHOICES,
	)

class Membership(models.Model):
	game = models.ForeignKey(
		Game,
		blank = False,
		on_delete = models.CASCADE,
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		blank = False,
		on_delete = models.CASCADE,
	)
	current_target = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null = True,
		on_delete = models.SET_NULL,
		related_name = 'assassins',
	)
	is_alive = models.BooleanField(
		default = True,
	)

	MEMBERSHIP_CHOICES = (
		(0, 'Confirmed'),
		(1, 'Invited'),
		(2, 'Requested'),
	)
	membership_status = models.PositiveIntegerField(
		blank = False,
		choices = MEMBERSHIP_CHOICES,
	)
	is_admin = models.BooleanField(
		default = False,
	)
