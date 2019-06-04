from django.contrib import admin
from .models import *

class SubmitInline(admin.StackedInline):
    model = Submit

class TeamUserInline(admin.StackedInline):
    model = TeamUser

class TeamSubmitInline(admin.StackedInline):
    model = TeamSubmit

class UsernameAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username', 'solved', 'last_solved_time']}),
	]
	inlines = [SubmitInline, TeamUserInline]
	list_display = ('id', 'username', 'solved', 'last_solved_time')
	list_filter = ['username', 'solved']
	search_fields = ['username']

class ChallengeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'type', 'flag', 'solved', 'description', 'is_ctf', 'score']}),
	]
	inlines = [SubmitInline, TeamSubmitInline]
	list_display = ('id', 'type', 'name', 'solved', 'is_ctf', 'score')
	list_filter = ['type', 'name', 'solved', 'is_ctf', 'score']
	search_fields = ['type', 'name']

class SubmitAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username', 'challenge', 'submit_time']}),
	]
	list_display = ('id', 'username', 'challenge', 'submit_time')
	list_filter = ['username', 'challenge']
	search_fields = ['username', 'challenge']

class TeamAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['teamname', 'token', 'score', 'solved', 'last_solved_time']}),
	]
	inlines = [TeamUserInline, TeamSubmitInline]
	list_display = ('id', 'teamname', 'token', 'score', 'solved', 'last_solved_time')
	list_filter = ['teamname', 'score', 'solved']
	search_fields = ['teamname', 'score']

class TeamUserAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['team', 'username']}),
	]
	list_display = ('id', 'team', 'username')
	list_filter = ['team', 'username']
	search_fields = ['team', 'username']

class TeamSubmitAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['team', 'challenge', 'submit_time']}),
	]
	list_display = ('id', 'team', 'challenge', 'submit_time')
	list_filter = ['team', 'challenge']
	search_fields = ['team', 'challenge']

admin.site.register(Username, UsernameAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Submit, SubmitAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamUser, TeamUserAdmin)
admin.site.register(TeamSubmit, TeamSubmitAdmin)