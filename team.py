from index.models import *

team_list = [
	("{teamname}", ["{teamUser}", "{teamUser}", "{teamUser}", "{teamUser}"]),
]

def getUsername(username):
	if not Username.objects.filter(username=username).exists():
		username = Username.objects.create(username=username)
	else: username = Username.objects.get(username=username)
	return username

for teamname, username_list in team_list:
	username = getUsername(username_list[0])
	Team.create(teamname=teamname, username=username)
	team = Team.objects.get(teamname=teamname)
	for username in username_list[1:]:
		username = getUsername(username)
		TeamUser.create(team=team, username=username)