from __future__ import absolute_import

from celery import shared_task
from random import shuffle

@shared_task
def start_game(game):
	game.start_game()

@shared_task
def end_round(game):
	game.end_round()
