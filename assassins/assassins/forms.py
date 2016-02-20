from django import forms

class KilledUsernameForm(forms.Form):
	username = forms.CharField(
		max_length = 30,
	)

