from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *

def is_login(request):
	if 'username' in request.session.keys():
		if len(request.session['username']) > 0: return True
		else: return False
	else: return False

def index(request):
	challenge_list = Challenge.objects.all()
	submit_list = Submit.objects.all()
	if is_login(request):
		challenge_list = []
		username = Username.objects.get(username=request.session['username'])
		for challenge in Challenge.objects.all():
			challenge.user_solve = Submit.objects.filter(username=username, challenge=challenge).exists()
			challenge_list.append(challenge)
	return render(request, "index.html", 
		{
			'key': is_login(request),
			'challenge_list': challenge_list,
			'submit_list': submit_list
		}
	)

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		if Username.objects.filter(username=username).exists(): 
			user = Username.objects.get(username=username)
		else: user = Username.objects.create(username=username)
		request.session['username'] = user.username
	return redirect("/scoreboard")

def flag(request):
	if request.method == 'POST':
		flag = request.POST.get('flag')
		if Challenge.objects.filter(flag=flag).exists():
			username = Username.objects.get(username=request.session['username'])
			challenge = Challenge.objects.get(flag=flag)
			if not Submit.objects.filter(username=username, challenge=challenge).exists():
				Submit.objects.create(username=username, challenge=challenge)
				username.solved += 1
				username.save()
				challenge.solved += 1
				challenge.save()
			else: return HttpResponse("<script>alert('你已經解過此題');window.location = '/scoreboard';</script>")
		else: return HttpResponse("<script>alert('flag錯誤');window.location = '/scoreboard';</script>")
	else: return HttpResponse("<script>alert('bad hacker!!');window.location = '/scoreboard';</script>")
