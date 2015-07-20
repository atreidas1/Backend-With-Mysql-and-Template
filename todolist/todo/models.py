from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task = models.CharField(max_length=200)
    deadline = models.DateField('date published')
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):              # __unicode__ on Python 2
        return self.task

