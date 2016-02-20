from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

# Create your views here.
def index(request):
	return render(request, 'assassins/index.html')

def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return auth_views.login(request)
