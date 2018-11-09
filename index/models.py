from django.db import models

class Username(models.Model):
	username = models.CharField(max_length=100, null=False, blank=False)
	solved = models.IntegerField(default=0)

	def __str__(self):
		return "username: {}; solved: {}".format(username, str(solved))

class Challenge(models.Model):
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=100, default='misc')
	flag = models.CharField(max_length=100)
	solved = models.IntegerField(default=0)
	description = models.CharField(max_length=100)
	user_solve = models.BooleanField(default=False)

	def __str__(self):
		return "name: {}; type: {}; solved: {}".format(name, type, str(solved))

class Submit(models.Model):
	username = models.ForeignKey(Username, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

	def __str__(self):
		return "username: {}; challenge: {}".format(username.__str__(), challenge.__str__())