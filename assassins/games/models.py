from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from datetime import datetime
from random import shuffle

from games.tasks import start_game, end_round

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

	def start_game(self):
		if self.membership_set.count() <= 1:
			pass #TODO

		self.drop_unconfirmed_players()
		self.assign_targets()
		self.notify_game_start()
		self.schedule_new_round()

	def end_round(self):
		self.resolve_protests()
		self.drop_stagnated_players()
		self.assign_targets()
		if self.membership_set.count() > 1:
			self.schedule_new_round()

	def drop_unconfirmed_players(self):
		self.membership_set.exclude(membership_status=0).delete()

	def assign_targets(self):
		players = list(self.membership_set.all())
		shuffle(players)

		if len(players) == 0:
			return

		for i in range(len(players) - 1):
			players[i].current_target = players[i + 1]
			players[i].save()
		players[-1].current_target = players[0]
		players[-1].save()

	def notify_game_start(self):
		pass

	def schedule_new_round(self):
		self.description = 'celery says hi'
		self.save()
		end_round.apply_async(args=[self], eta=datetime.now() + self.round_length)

	def resolve_protests(self):
		pass

	def drop_stagnated_players(self):
		stagnants = []
		for m in self.membership_set.filter(is_alive=True):
			if m.is_stagnant(self):
				stagnants.append(m)

		m = self.membership_set.filter(is_alive=True).first()

		while stagnants:
			next_m = m.current_target
			if m in stagnants:
				assassin = m.user.assassins.get(game=self)
				assassin.current_target = m.current_target
				assassin.save()

				m.is_alive = False
				m.current_target = None
				m.save()
				stagnants.remove(m)

				next_m = assassin.current_target

			m = self.membership_set.get(is_alive=True, user=next_m, game=self)


@receiver(post_save, sender=Game)
def save_game(sender, instance, created, **kwargs):
	if created:
		start_game.apply_async(args=[instance], eta=instance.start_date)


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

	class Meta:
		unique_together = ('game', 'user')
		index_together = ['game', 'user']

	def is_stagnant(self, game):
		target = Membership.objects.get(game=game, user=self.current_target)
		return target.is_alive and self.is_alive
