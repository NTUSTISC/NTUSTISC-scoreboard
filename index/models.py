from django.db import models
from django.utils import timezone

class Username(models.Model):
	username = models.CharField(max_length=100, null=False, blank=False)
	solved = models.IntegerField(default=0)
	last_solved_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "username: {}; solved: {};".format(self.username, self.solved)

class Challenge(models.Model):
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=100, default='misc')
	flag = models.CharField(max_length=250)
	solved = models.IntegerField(default=0)
	description = models.CharField(max_length=100)
	user_solve = models.BooleanField(default=False)

	def __str__(self):
		return "name: {}; type: {}; solved: {}".format(self.name, self.type, str(self.solved))

class Submit(models.Model):
	username = models.ForeignKey(Username, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

	def __str__(self):
		return "username: {}; challenge: {}".format(self.username.__str__(), self.challenge.__str__())