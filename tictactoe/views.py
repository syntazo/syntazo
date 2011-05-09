# Python imports
import logging
import datetime
import urllib
import sys

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
import TicTacToe
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


def index(request):
  logging.info('cookies: '+str(request.COOKIES))

  #return http.HttpResponse('No app with that id')
  return respond(request, None, 'tictactoe', {})
  
def get_supported_games(request):
    result = {'tictactoe':'http://localhost:8081/tictactoe'}
    return http.HttpResponse(json.dumps(result))

def get_new_board(request):
    player = TicTacToe.TicTacToe()
    result = player.get_new_board()
    return http.HttpResponse(json.dumps(result))

def get_input_from_request(request):
    #Get a board out of the POST or GET
    jsonrequest = None
    if request.GET:
        jsonrequest = request.GET.get('jsonrequest')
    
    if request.POST:
        jsonrequest = request.POST.get('jsonrequest')
    
    if not jsonrequest:
        return {'error': 'No jsonrequest passed in.'}
    
    #Add try and catch to handle bad JSON
    input = None
    try:
        input = json.loads(jsonrequest)
    except:
        e = sys.exc_info()[1]
        return {'error': 'Problem parsing passed in json.'+str(e)}
     
    return input
 
def is_board_valid(request):
    #Get a board out of the POST or GET
    input = get_input_from_request(request)
    if input.has_key('error'):
        return http.HttpResponse('Problem parsing passed in json.'+input['error']) 
 
    board = input['board']
    player = TicTacToe.TicTacToe()
    result = player.is_board_valid(board)
    return http.HttpResponse(json.dumps(result))

def game_status(request):
    #Get a board out of the POST or GET
    input = get_input_from_request(request)
    if input.has_key('error'):
        return http.HttpResponse('Problem parsing passed in json.'+input['error']) 
 
    board = input['board']
    player = TicTacToe.TicTacToe()
    result = player.game_status(board)
    return http.HttpResponse(json.dumps(result))

def get_next_move(request):
    #Get move and board from POST or GET
    input = get_input_from_request(request)
    if input.has_key('error'):
        return http.HttpResponse('Problem parsing passed in json.'+input['error']) 

    player = TicTacToe.RandomTicTacToe()
    #player = TicTacToe.TicTacToe()
    board = input['board']
   
#    if request.GET:
#        alternate = request.GET.get('alternate')
#    if alternate:
#        players = [TicTacToe.TicTacToe(), TicTacToe.CenterGrabTicTacToe(), TicTacToe.RandomTicTacToe(),TicTacToe.CenterGrabRandomTicTacToe(),TicTacToe.BottomUpTicTacToe(), TicTacToe.HunterTicTacToe()]
#        index = int(alternate)
#        player = players[index]        

    result = player.get_next_move(board)
    return http.HttpResponse(json.dumps(result))

def is_move_valid(request):
    #Get move and board from POST or GET
    input = get_input_from_request(request)
    if input.has_key('error'):
        return http.HttpResponse('Problem parsing passed in json.'+input['error']) 
    
    player = TicTacToe.TicTacToe()
    board = input['board']
    move = input['move']
    result = player.is_move_valid(board,move)
    return http.HttpResponse(json.dumps(result))
  
