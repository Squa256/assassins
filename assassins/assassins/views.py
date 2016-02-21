from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from assassins.forms import KilledUsernameForm
from games.models import Membership
from users.models import User

# Create your views here.
def claim_kill(request):
	killed_username_form = KilledUsernameForm(request.POST)
	if killed_username_form.is_valid():
		killed_user = User.objects.get(username=killed_username_form.cleaned_data['username'])
		member = Membership.objects.get(user=killed_user)
		member.is_alive = False
		member.save()
	else:
		#TODO: Handle invalid form
		pass

def confirm_or_deny_kill(request):
	if request.POST.get('confirm'):
		Membership.objects.get(user=request.user).delete()
	elif request.POST.get('deny'):
		#Set 24 hour timer until user is removed
		pass

def index(request):
	if request.user.is_authenticated():
		memberships = Membership.objects.filter(user=request.user)

		if request.method == 'POST':
			if request.POST.get('username'):
				claim_kill(request)
			else:
				confirm_or_deny_kill(request)

		return render(request, 'assassins/home.html',{
			'memberships': memberships,
			'killed_username_form': KilledUsernameForm(),
			'user': request.user,
		})

	return render(request, 'assassins/index.html')

def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return auth_views.login(request)
