from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *

def is_login(request):
    if 'username' in request.session.keys():
        if len(request.session['username']) > 0:
            return True
        else:
            return False
    else:
        return False


def index(request):
    message = messages.get_messages(request)
    challenge_list = Challenge.objects.all().order_by('type', 'id')
    submit_list = Submit.objects.all().order_by('-id')[:20]
    rank = Username.objects.all().order_by('-solved')[:10]
    logined = is_login(request)
    username = None
    if logined:
        challenge_list = []
        username = Username.objects.get(username=request.session['username'])
        for challenge in Challenge.objects.all().order_by('type', 'id'):
            challenge.user_solve = Submit.objects.filter(
                username=username,
                challenge=challenge
            ).exists()
            challenge_list.append(challenge)
    return render(request, "index.html", {
        'key': logined,
        'username': username,
        'solving_rate': int(username.solved / len(challenge_list) * 100) if username else 0,
        'rank': rank,
        'challenge_list': challenge_list,
        'submit_list': submit_list
    })


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username.strip() == "":
            return redirect("../")
        if Username.objects.filter(username=username).exists():
            user = Username.objects.get(username=username)
        else:
            user = Username.objects.create(username=username)
        request.session['username'] = user.username
    return redirect("../")

def logout(request):
    del request.session['username']
    return redirect("../")

def flag(request):
    if request.method == 'POST':
        flag = request.POST.get('flag').strip()
        if Challenge.objects.filter(flag=flag).exists():
            username = Username.objects.get(
                username=request.session['username'])
            challenge = Challenge.objects.get(flag=flag)
            if not Submit.objects.filter(username=username, challenge=challenge).exists():
                Submit.objects.create(username=username, challenge=challenge)
                username.solved += 1
                username.save()
                challenge.solved += 1
                challenge.save()
                messages.add_message(request, messages.SUCCESS, "Flag 正確！")
                return redirect('../')
            else:
                messages.add_message(request, messages.INFO, "Flag 是正確沒錯啦，但你已經解過這題了")
                return redirect('../')
        else:
            messages.add_message(request, messages.ERROR, "Flag 錯誤 QQ")
            return redirect('../')
    else:
        challenge = Challenge.objects.get(name="Just Here")
        return HttpResponse("""
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
                <title>405 Method Not Allowed</title>
                <h1>Method Not Allowed</h1>
                <p>The method is not allowed for the requested URL.</p>
                <!-- {0} -->
                """.format(challenge.flag))
