# Python imports
import logging

# AppEngine imports
#from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from google.appengine.api import memcache
from google.appengine.api import quota
from google.appengine.api.labs import taskqueue

#import django
from django import http
from django import shortcuts
from django.utils import simplejson as json
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import Site
from django.utils.http import urlencode as django_urlencode

# Local imports
import models
from forms import CourseForm, AppForm
import base64
from myutil import common

def respond(request, user, template, params=None):
  """Helper to render a response, passing standard stuff to the response.

  Args:
    request: The request object.
    user: The User object representing the current user; or None if nobody
      is logged in.
    template: The template name; '.html' is appended automatically.
    params: A dict giving the template parameters; modified in-place.

  Returns:
    Whatever render_to_response(template, params) returns.

  Raises:
    Whatever render_to_response(template, params) raises.
  """
  ip = request.META['REMOTE_ADDR']
  if params is None:
    params = {}
  
  if user:
    params['user'] = user
    params['sign_out'] = models.User.create_logout_url('/')
    params['is_admin'] = (user.is_current_user_admin())
#  else:
#    params['sign_in'] = models.User.create_login_url(request.path)
  params['domain_url'] = common.getHostURI(request)
  params['page'] = template
  
  if not template.endswith('.html'):
    template += '.html'
  response = direct_to_template(request, template, params)
#  if user:
#    common.set_cookie(response = response, name = 'user_id', value = user.user_id)
  return response

def get_user(request):
  user = None
  if 'session_id' in request.COOKIES:
    session_id = request.COOKIES['session_id']
    session_id = base64.b64decode(session_id)
    logging.info('got session_id in cookies: '+str(session_id))
    session = models.Session.get_session(session_id)
    if session:
        user = models.User.get_current_user(session.user_id)
  if not user:
    logging.warning('User not logined')
  return user

#Move this to a template. 
def auth_error(domain_url):
  return http.HttpResponse(content = 
      '''<html><body>
          You are not logined! You can <a class="rpxnow" onclick="return false;" href="https://pivotalexpert.rpxnow.com/openid/v2/signin?token_url='''+domain_url+'''%2Frpx.php">sign in here</a>!
          <script type="text/javascript">
            var rpxJsHost = (("https:" == document.location.protocol) ? "https://" : "http://static.");
            document.write(unescape("%3Cscript src='" + rpxJsHost + "rpxnow.com/js/lib/rpx.js' type='text/javascript'%3E%3C/script%3E"));
          </script>
          <script type="text/javascript">
            RPXNOW.overlay = true;
            RPXNOW.language_preference = 'en';
          </script>
         </body>
         </html>''', status = 401)

def index(request):
  logging.info('cookies: '+str(request.COOKIES))
  user = get_user(request)
  #if not user:
  #  return auth_error(common.getHostURI(request))
  courses = models.Course.all()
  apps = models.App.all()
  return respond(request, user, 'index', {'next': '/', 'courses':courses, 'apps':apps})
  
def add_course(request):
  #Fetch name parameter from GET request and create new course as an example
  logging.info('Adding a course')
  user = get_user(request)
  #if not user:
  #  return auth_error(common.getHostURI(request))
  models.Course.add_course(name='New Course', user=user)
  courses = models.Course.all()
  return respond(request, user, 'index', {'next': '/', 'courses':courses})

def add_app(request):
  #Fetch name parameter from GET request and create new course as an example
  logging.info('Adding an app')
  user = get_user(request)
  #if not user:
  #  return auth_error(common.getHostURI(request))
  models.App.add_app(name='New App', user=user, url='http://www.google.com')
  courses = models.Course.all()
  apps = models.App.all()
  return respond(request, user, 'index', {'next': '/', 'courses':courses, 'apps':apps})
  
def courses(request):
    courses = models.Course.all()

    #Update the view to list supported and unsupported interfaces.
    return respond(request,None,'courses', {'courses':courses})
  
def edit_course(request, course_id=None):
  logging.info("In edit course")
  #currentPlayer = models.Player.get_the_current_player()
  
  #if currentPlayer is None:
  #  return http.HttpResponseForbidden('You must be an signed in to create/edit an interface.')

  course = None
  creatingNew = False
  
  if not course_id:
    creatingNew = True
    
  else:
    course = models.Course.get_by_id(int(course_id))
    if course is None:
      return http.HttpResponseNotFound('No such course.') 
    #if interface.editor.key().id() != currentPlayer.key().id() and not models.Player.is_current_player_admin():
    #  return http.HttpResponseForbidden('You can only edit your own interfaces.')

  form = CourseForm(data=request.POST or None, instance=course)

  if not request.POST:
    return respond(request, None, 'edit_course', {'form': form, 'course': course, 'creatingNew': creatingNew})
  
  errors = form.errors
  if not errors:
    try:
        course = form.save(commit=False)
    except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return respond(request, None, 'edit_course', {'form': form, 'course': course, 'creatingNew': creatingNew})
  else:
      logging.info("There were form.errors. %s", errors)

  if creatingNew:
    pass
    #path.owner = user
    #interface.editor = currentPlayer
    #interface.owner = 'scboesch'
    #interface.singpathSupported = False

  course.put()
  return http.HttpResponseRedirect('/')
  

