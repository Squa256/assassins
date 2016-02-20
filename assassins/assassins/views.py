from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from assassins.forms import KilledUsernameForm
from games.models import Membership
from users.models import User

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		targets = Membership.objects.filter(user=request.user)

		if request.method == 'POST':
			killed_username_form = KilledUsernameForm(request.POST)
			if killed_username_form.is_valid():
				print("Killing user", killed_username_form.cleaned_data['username'])
				user = User.objects.get(username=killed_username_form.cleaned_data['username'])
				member = Membership.objects.get(user=user)
				member.is_alive = False
				member.save()
		else:
			killed_username_form = KilledUsernameForm()

		return render(request, 'assassins/home.html', {
			'targets': targets,
			'user': request.user,
			'killed_username_form': killed_username_form,
		})

	return render(request, 'assassins/index.html')

def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return auth_views.login(request)
