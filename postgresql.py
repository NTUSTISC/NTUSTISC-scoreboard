from django.conf import settings
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from index.models import Challenge, Username, Submit

import pytz

challenge_map = {}
username_map = {}

def sql_sort(table_name):
	table_names = open("postgresql/{table_name}.sql".format(table_name=table_name), "r").read().split("\n")
	table_names = list(map(lambda x: x.split("\t"), table_names))
	table_names.sort(key=lambda x: int(x[0]))
	open("postgresql/{table_name}.sql".format(table_name=table_name), "w").write(
		"\n".join(map(lambda x: '\t'.join(x), table_names))
	)
	return table_names

def create_challenge(challenge_list):
	global Challenge, challenge_map
	for id, name, flag, solved, description, _, type in challenge_list:
		challenge = Challenge.objects.create(
			name=name, flag=flag, solved=int(solved), description=description, type=type,
			is_ctf=(int(id)>=38), score=500*(int(id)>=38)
		)
		challenge_map[id] = challenge

def create_username(username_list):
	global Username, parse_datetime, pytz, settings, username_map
	for id, username, solved, last_solved_time  in username_list:
		username = Username.objects.create(
			username=username, solved=int(solved),
			last_solved_time=pytz.timezone(settings.TIME_ZONE).localize(
				parse_datetime(last_solved_time.split(".")[0]), is_dst=None
			)
		)
		username_map[id] = username

def create_submit(submit_list):
	global Submit
	for _, challenge_id, username_id in submit_list:
		Submit.objects.create(
			challenge=challenge_map[challenge_id],
			username=username_map[username_id]
		)

E = [
	("challenge", create_challenge),
	("username", create_username),
	("submit", create_submit)
]

if settings.SHELL:
	for table, function in E:
		function(sql_sort(table))
		print("Insert {table} Data Success.".format(table=table))
