from django.http import Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from assassins import views as assassin_views
from users.forms import CreateUserForm
from users.models import User

def profile(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		raise Http404
	return render(request, 'users/profile.html', {'user': user})

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
