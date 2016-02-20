from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
	pass

@require_POST
def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		return auth_views.login(request)
