from django.contrib import admin

from .models import Task

class TaskAdmin(admin.ModelAdmin):
    fields = ['task', 'deadline','status','user']

admin.site.register(Task, TaskAdmin)
