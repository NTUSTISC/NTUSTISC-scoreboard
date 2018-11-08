from django.contrib import admin
from .models import *

class UsernameAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['user', 'name', 'skype', 'detail', 'picture']}),
	]
	inlines = [BookInline, CourseInline]
	list_display = ('id', 'user', 'name')
	list_filter = ['user', 'name']
	search_fields = ['user', 'name']

class ChallengeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['user', 'name', 'skype', 'detail', 'picture']}),
	]
	inlines = [BookInline, CourseInline]
	list_display = ('id', 'user', 'name')
	list_filter = ['user', 'name']
	search_fields = ['user', 'name']

class SubmitAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['user', 'name', 'skype', 'detail', 'picture']}),
	]
	inlines = [BookInline, CourseInline]
	list_display = ('id', 'user', 'name')
	list_filter = ['user', 'name']
	search_fields = ['user', 'name']

admin.site.register(Username, UsernameAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Submit, SubmitAdmin)