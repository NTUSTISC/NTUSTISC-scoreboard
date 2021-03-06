from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import *

import os
import requests

def is_login(request):
    logined, teamed = False, False
    if 'username' in request.session.keys():
        if len(request.session['username']) > 0:
            if Username.objects.filter(username=request.session['username']).exists():
                logined = True
    if 'teamname' in request.session.keys():
        if len(request.session['teamname']) > 0:
            if Team.objects.filter(teamname=request.session['teamname']).exists():
                teamed = True
    return logined, teamed and settings.CTF

def telegram_message(message):
    link = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}".format(
        token=settings.TELEGRAM_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID, text=message
    )
    return requests.get(link).status_code == 200

@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html")

@require_http_methods(["GET"])
def scoreboard(request):
    challenge_list = []
    logined, teamed = is_login(request)
    message = messages.get_messages(request)
    submit_list = Submit.objects.all().order_by('-submit_time')[:20]
    rank_list = Username.objects.all().order_by('-solved', 'last_solved_time')[:10]
    team, username, solving_rate, teamuser_list = None, None, 0, []
    if teamed:
        team = Team.objects.get(teamname=request.session['teamname'])
        submit_list = TeamSubmit.objects.all().order_by('-submit_time')[:20]
        rank_list = Team.objects.all().order_by('-score', 'last_solved_time')[:10]
        username = Username.objects.get(username=request.session['username'])
        teamuser_list = TeamUser.objects.filter(team=team).order_by('username__username')
        for challenge in Challenge.objects.filter(is_ctf=True).order_by('type', 'id'):
            challenge.user_solve = TeamSubmit.objects.filter(team=team, challenge=challenge).exists()
            challenge_list.append((challenge, TeamSubmit.objects.filter(challenge=challenge)))
        solving_rate = int(team.solved / max(len(challenge_list), 1) * 100)
    elif logined:
        username = Username.objects.get(username=request.session['username'])
        for challenge in Challenge.objects.filter(is_ctf=False).order_by('type', 'id'):
            challenge.user_solve = Submit.objects.filter(username=username, challenge=challenge).exists()
            challenge_list.append((challenge, Submit.objects.filter(challenge=challenge)))
        solving_rate = int(username.solved / max(len(challenge_list), 1) * 100)
    else: 
        for challenge in Challenge.objects.filter(is_ctf=False).order_by('type', 'id'):
            challenge_list.append((challenge, Submit.objects.filter(challenge=challenge)))
    return render(request, "scoreboard.html", {
        'team': team,
        'ctfing': settings.CTF,
        'teamed': teamed,
        'logined': logined,
        'username': username,
        'rank_list': rank_list,
        'submit_list': submit_list,
        'solving_rate': solving_rate,
        'teamuser_list': teamuser_list,
        'challenge_list': challenge_list
    })

@require_http_methods(["POST"])
def login(request):
    username = request.POST.get('username').strip()
    if not 0 < len(username) <= 64:
        messages.add_message(request, messages.ERROR, "Invalid Username.")
        return redirect("/scoreboard")
    if Username.objects.filter(username=username).exists():
        username = Username.objects.get(username=username)
    else: username = Username.objects.create(username=username)
    if settings.CTF:
        teamname = request.POST.get('teamname').strip()
        if not 0 < len(teamname) <= 64:
            if len(teamname) > 64:
                messages.add_message(request, messages.ERROR, "Invalid Teamname.")
            return redirect("/scoreboard")
        if Team.objects.filter(teamname=teamname).exists():
            team = Team.objects.get(teamname=teamname)
            if not TeamUser.objects.filter(username=username).exists():
                token = request.POST.get('token').strip()
                if token == team.token:
                    if not TeamUser.create(username=username, team=team):
                        messages.add_message(request, messages.ERROR, "The Team is Full.")
                        return redirect("/scoreboard")
                    else: messages.add_message(request, messages.SUCCESS, "Team joined Success.")
                else:
                    messages.add_message(request, messages.ERROR, "Invalid Token.")
                    return redirect("/scoreboard")
            elif team != TeamUser.objects.get(username=username).team:
                messages.add_message(request, messages.INFO, "This Username has already joined Team.")
                return redirect('/scoreboard')
        else: 
            if not TeamUser.objects.filter(username=username).exists():
                Team.create(teamname=teamname, username=username)
            else:
                messages.add_message(request, messages.INFO, "This Username has already joined Team.")
                return redirect('/scoreboard')
        request.session['teamname'] = teamname
    request.session['username'] = username.username
    return redirect("/scoreboard")

@require_http_methods(["GET", "POST"])
def logout(request):
    try:
        del request.session['username']
        del request.session['teamname']
    except: pass
    finally: return redirect("/scoreboard")

@require_http_methods(["GET", "POST"])
def flag(request):
    logined, teamed = is_login(request)
    if request.method == 'POST' and logined:
        flag = request.POST.get('flag').strip()
        if Challenge.objects.filter(flag=flag, is_ctf=teamed).exists():
            username = Username.objects.get(username=request.session['username'])
            challenge = Challenge.objects.get(flag=flag, is_ctf=teamed)
            if not teamed:
                if not Submit.objects.filter(username=username, challenge=challenge).exists():
                    Submit.create(username=username, challenge=challenge)
                    telegram_message("@{} sloved {}".format(username.username, challenge.name))
                    messages.add_message(request, messages.SUCCESS, "Flag 正確！")
                    return redirect('/scoreboard')
                else:
                    messages.add_message(request, messages.INFO, "Flag 是正確沒錯啦，但你已經解過這題了")
                    return redirect('/scoreboard')
            else:
                team = Team.objects.get(teamname=request.session['teamname'])
                if not TeamSubmit.objects.filter(team=team, challenge=challenge).exists():
                    TeamSubmit.create(team=team, challenge=challenge)
                    telegram_message("{}@{} sloved {}".format(username.usermame, team.teamname, challenge.name))
                    messages.add_message(request, messages.SUCCESS, "Flag 正確！")
                    return redirect('/scoreboard')
                else:
                    messages.add_message(request, messages.INFO, "Flag 是正確沒錯啦，但你已經解過這題了")
                    return redirect('/scoreboard')
        else:
            messages.add_message(request, messages.ERROR, "Flag 錯誤 QQ")
            return redirect('/scoreboard')
    else:
        challenge = Challenge.objects.get(name="Just Here")
        return HttpResponse("""
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
                <title>405 Method Not Allowed</title>
                <h1>Method Not Allowed</h1>
                <p>The method is not allowed for the requested URL.</p>
                <!-- {0} -->
                """.format(challenge.flag))

@require_http_methods(["GET"])
def ctf_finish(request):
    if not settings.CTF:
        if not os.path.isfile("{Base}/{name}.json".format(base=settings.BASE_DIR, name=settings.CTF_NAME)):
            with open(settings.BASE_DIR + "/" + settings.CTF_NAME, "w") as file:
                file.write(serializers.serialize("json", Challenge.objects.filter(is_ctf=True).order_by("-score", "solved", "type", "name")) + "\n")
                file.write(serializers.serialize("json", Team.objects.all().order_by("-score", "-solved", "teamname")) + "\n")
                file.write(serializers.serialize("json", TeamUser.objects.all().order_by("-team__score", "-team__solved", "username__username")) + "\n")
                file.write(serializers.serialize("json", TeamSubmit.objects.all().order_by("-submit_time")) + "\n")
            for team in Team.objects.all():
                team.delete()
            for challenge in Challenge.objects.filter(is_ctf=True):
                challenge.finish()
        return HttpResponse("CTF is finish!")
    else:
        return HttpResponse("CTF is ongoing!")