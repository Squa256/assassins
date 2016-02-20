from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from games.models import Membership

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		targets = Membership.objects.filter(user=request.user)
		return render(request, 'assassins/home.html',
				{'user': request.user, 'targets': targets})

	return render(request, 'assassins/index.html')

def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return auth_views.login(request)
