from django.forms import ModelForm

from games.models import Game

class CreateGameForm(ModelForm):
	class Meta:
		model = Game
		fields = ['name', 'description', 'start_date', 'round_length',
			'approval_preference', 'max_num_players']

