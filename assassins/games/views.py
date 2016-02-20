from django.shortcuts import render, redirect
from games.forms import CreateGameForm
from games.models import Game, Membership

# Create your views here.
def homepage(request, game_id):
	game = Game.objects.get(id=game_id)
	memberships = Membership.objects.filter(game=game)
	return render(request, 'games/homepage.html',
			{'game': game, 'memberships': memberships})

def create(request):
	if request.method == 'POST':
		form = CreateGameForm(request.POST)
		if form.is_valid():
			new_game = form.save()
			new_game_id = new_game.id
			return redirect('games:homepage', game_id=new_game_id)
	else:
		form = CreateGameForm()

	return render(request, 'games/create.html', {'form': form})
