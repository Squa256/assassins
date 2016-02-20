from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from assassins import views as assassin_views
from forms import CreateUserForm
from models import User

# Create your views here.
def profile(request, user_id):
	pass

def create(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			new_user = authenticate(username=form.cleaned_data['username'],
					password=form.cleaned_data['password1'])
			login(request, new_user)
			return redirect('index')
	else:
		form = CreateUserForm()

	return render(request, 'users/create.html', {'form': form})
