from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from todo.models import Task
from tastypie.authentication import SessionAuthentication


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication = SessionAuthentication()
        #fields = ['username', 'first_name', 'last_name', 'last_login']
        #allowed_methods = ['get']


class TaskResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Task.objects.all()
        resource_name = 'tasks'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
