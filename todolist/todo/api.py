from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from todo.models import Task
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization,Authorization
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import  url
from tastypie.utils import trailing_slash
from django.core.exceptions import ObjectDoesNotExist
from authorization import UsersAuthorization, TasksAuthorization


###################User resource####################

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization=UsersAuthorization()
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser','last_login','last_name',
                    'date_joined','first_name']
        #allowed_methods = ['get']
        filtering = {
            'username': ALL,
        }

###################Task resource####################

class TaskResource(ModelResource):
  user = fields.ForeignKey(UserResource, 'user')

  class Meta:
    authorization = TasksAuthorization() #Authorization()
    queryset = Task.objects.all()
    allowed_methods = ['get', 'post', 'put','patch','delete']
    resource_name = 'tasks'
    always_return_data=True
    filtering = {
            'user': ALL_WITH_RELATIONS,
        }


###################Login resource####################

class LoginResource(Resource):
  class Meta:
    resource_name = 'login'

  def dispatch(self, request_type, request, **kwargs):
    self.method_check(request, allowed=['post'])
    data = self.deserialize(request, request.body,
                            format=request.META.get('CONTENT_TYPE', 'application/json'))
    username = data.get('username', '')
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request,user)
        return self.create_response(request, {
                    'success': True
                    })
      else:
        return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
    else:
      return self.create_response(request, {
                  'success': False,
                  'reason': 'incorrect',
                  }, HttpUnauthorized )


###################Logout resource####################
class LogoutResource(Resource):
  class Meta:
    allowed_methods = ['get']
    resource_name = 'logout'

  def dispatch(self, request_type, request, **kwargs):
    if request.user and request.user.is_authenticated():
      logout(request)
      return self.create_response(request, { 'success': True })
    else:
      return self.create_response(request, { 'success': False }, HttpUnauthorized)

###################Register resource####################

class RegisterResource(Resource):
  class Meta:
    resource_name = 'register'

  def dispatch(self, request_type, request, **kwargs):
    self.method_check(request, allowed=['post'])
    data = self.deserialize(request, request.body,
                            format=request.META.get('CONTENT_TYPE', 'application/json'))
    username = data.get('username', '')
    password = data.get('password', '')
    repeatPassword = data.get('repeatpassword', '')
    if username is not None:
      try:
        user=User.objects.get(username=username)
        return self.create_response(request, { 'success' : False,
                                               'reason' : 'userexist' })
      except ObjectDoesNotExist:
        if password == repeatPassword:
          user =  User.objects.create_user(username, username+'@thebeatles.com', password)
          user.save()
          return self.create_response(request, { 'success' : True})
        else:
          return self.create_response(request, { 'success' : False,
                                                  'reason' : 'differentpass'})
    else:
      return self.create_response(request, { 'success' : False,
                                             'reason' : 'nousername'})
