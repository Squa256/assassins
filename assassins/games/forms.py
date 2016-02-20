from django import forms

from games.models import Game, Membership

class CreateGameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ['name', 'description', 'start_date', 'round_length',
			'approval_preference', 'max_num_players']

class AddUsernameForm(forms.Form):
	username = forms.CharField(
		max_length = 30,
	)
