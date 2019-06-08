from django.db import models
from django.utils import timezone

from os import urandom
from math import exp
from binascii import hexlify

score_func = lambda x: max(int(1000 / (1 + exp(3 * x))), 100)

class Username(models.Model):
	username = models.CharField(max_length=100, null=False, blank=False)
	solved = models.IntegerField(default=0)
	last_solved_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "username: {}; solved: {};".format(self.username, self.solved)

	def solve(self):
		self.solved += 1
		self.last_solved_time = timezone.now()
		self.save()

	def create(username):
		Username.objects.create(username=username)

class Challenge(models.Model):
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=100, default='misc')
	flag = models.CharField(max_length=250)
	solved = models.IntegerField(default=0)
	description = models.CharField(max_length=100)
	user_solve = models.BooleanField(default=False)
	is_ctf = models.BooleanField(default=False)
	score = models.IntegerField(default=0)

	def __str__(self):
		return "name: {}; type: {}; solved: {}".format(self.name, self.type, str(self.solved))

	def solve(self):
		self.solved += 1
		self.save()

	def finish(self):
		self.is_ctf = False
		self.solved = 0
		self.score = 0
		self.save()

	def rescore(self):
		self.score = score_func(max(self.solved - 1, 0) / len(Team.objects.all()))
		self.save()

class Submit(models.Model):
	username = models.ForeignKey(Username, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	submit_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "username: {}; challenge: {}; submit_time: {}".format(
			self.username.__str__(),
			self.challenge.__str__(),
			self.submit_time
		)

	def create(username, challenge):
		Submit.objects.create(username=username, challenge=challenge)
		username.solve()
		challenge.solve()

class Team(models.Model):
	teamname = models.CharField(max_length=100, null=False, blank=False)
	token = models.CharField(max_length=10)
	score = models.IntegerField(default=0)
	solved = models.IntegerField(default=0)
	last_solved_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "teamname: {}; score: {}; solved: {};".format(
			self.teamname, str(self.score), str(self.solved)
		)

	def solve(self):
		self.solved += 1
		self.last_solved_time = timezone.now()
		self.save()

	def rescore(self, score_delta):
		self.score += score_delta
		self.save()

	def create(teamname, username):
		token = str(hexlify(urandom(5)), "utf-8")
		team = Team.objects.create(teamname=teamname, token=token)
		TeamUser.create(team=team, username=username)
		for challenge in Challenge.objects.filter(is_ctf=True):
			old_score = challenge.score
			challenge.rescore()
			score_delta = challenge.score - old_score
			for teamSubmit in TeamSubmit.objects.filter(challenge=challenge):
				teamSubmit.team.rescore(score_delta)

class TeamUser(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	username = models.ForeignKey(Username, on_delete=models.CASCADE)

	def __str__(self):
		return "team: {}; username: {}".format(
			self.team.__str__(),
			self.username.__str__()
		)

	def create(team, username):
		if len(TeamUser.objects.filter(team=team)) < 4:
			TeamUser.objects.create(team=team, username=username)
			return True
		return False

class TeamSubmit(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	submit_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "team: {}; challenge: {}; submit_time: {}".format(
			self.team.__str__(),
			self.challenge.__str__(),
			self.submit_time
		)

	def create(team, challenge):
		TeamSubmit.objects.create(team=team, challenge=challenge)
		old_score = challenge.score
		team.solve()
		challenge.solve()
		challenge.rescore()
		team.rescore(old_score)
		score_delta = challenge.score - old_score
		for teamSubmit in TeamSubmit.objects.filter(challenge=challenge):
			teamSubmit.team.rescore(score_delta)
