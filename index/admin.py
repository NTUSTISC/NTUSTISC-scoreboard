from django.contrib import admin
from .models import *

class SubmitInline(admin.StackedInline):
    model = Submit

class UsernameAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username', 'solved', 'last_solved_time']}),
	]
	inlines = [SubmitInline]
	list_display = ('id', 'username', 'solved', 'last_solved_time')
	list_filter = ['username', 'solved', 'last_solved_time']

class ChallengeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'type', 'flag', 'solved', 'description']}),
	]
	inlines = [SubmitInline]
	list_display = ('id', 'type', 'name', 'solved')
	list_filter = ['type', 'name', 'solved']

class SubmitAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['username', 'challenge']}),
	]
	list_display = ('id', 'username', 'challenge')
	list_filter = ['username', 'challenge']
	search_fields = ['username', 'challenge']

admin.site.register(Username, UsernameAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Submit, SubmitAdmin)