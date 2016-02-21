from django.http import Http404
from django.shortcuts import render, redirect
from games.forms import CreateGameForm, AddUsernameForm
from games.models import Game, Membership
from users.models import User

# Create your views here.
def homepage(request, game_id):
	try:
		game = Game.objects.get(id=game_id)
	except Game.DoesNotExist:
		raise Http404('Game does not exist')

	if  request.method == 'POST':
		add_username_form = AddUsernameForm(request.POST)
		if add_username_form.is_valid():
			try:
				user = User.objects.get(username=add_username_form.cleaned_data['username'])
			except User.DoesNotExist:
				raise Http404('User does not exsist')
			new_membership = Membership.objects.create(
				user=user,
				game=game, 
				membership_status=1,
			)
	else:
		add_username_form = AddUsernameForm()

	memberships = Membership.objects.filter(game=game)

	return render(request, 'games/homepage.html', {
		'game': game,
		'memberships': memberships,
		'add_username_form': add_username_form,
	})

def create(request):
	if request.method == 'POST':
		form = CreateGameForm(request.POST)
		if form.is_valid():
			new_game = form.save()
			return redirect('games:homepage', game_id=new_game.id)
	else:
		form = CreateGameForm()

	return render(request, 'games/create.html', {'form': form})
