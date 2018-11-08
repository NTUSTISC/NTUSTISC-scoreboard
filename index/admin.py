from django.contrib import admin
from .models import *

class UsernameInline(admin.StackedInline):
    model = Username

class ChallengeInline(admin.StackedInline):
    model = Challenge

class UsernameAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username']}),
	]
	list_display = ('id', 'username')

class ChallengeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'type', 'flag', 'solved', 'description']}),
	]
	list_display = ('id', 'type', 'name', 'solved')
	list_filter = ['type', 'name', 'solved']

class SubmitAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username', 'challenge']}),
	]
	inlines = [UsernameInline, ChallengeInline]
	list_display = ('id', 'username', 'challenge')
	list_filter = ['username', 'challenge']
	search_fields = ['username', 'challenge']

admin.site.register(Username, UsernameAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Submit, SubmitAdmin)