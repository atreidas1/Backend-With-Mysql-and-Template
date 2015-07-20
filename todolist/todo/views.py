from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from models import Task

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def tasks_listing(request):
    """A view of all tasks."""
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})
