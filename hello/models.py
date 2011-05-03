from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import quota
from google.appengine.api import memcache

import logging
import datetime
import urllib
import random
#from aeoid import users
from google.appengine.api import users
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from google.appengine.api.labs import taskqueue

#from django.utils.hashcompat import md5_constructor
from django.utils.html import escape
from operator import itemgetter

class User(db.Model):
    user_id = db.StringProperty(required=True)
    nickname = db.StringProperty(required=False)
    email = db.StringProperty(required=False)
    pic_url = db.StringProperty(required=False)

    @staticmethod
    def get_current_user(user_id, nickname=None, email=None):
        if not user_id:
            return None
        user = User.all().filter('user_id =', user_id).get()
        if not user:
            user = User(user_id = user_id, nickname = nickname, email = email)
            user.put()
        return user

    @staticmethod
    def login(user_id, nickname=None, email=None):
        user = User.get_current_user(user_id, nickname, email)
        if not user:
            raise Exception('Login unsuccessful')
        return user
    
    @staticmethod
    def is_current_user_admin():
        return False
    
    @staticmethod
    def create_logout_url(target):
        return '/logout?target=' + str(target)
    
    @staticmethod
    def create_login_url(target):
        return '/login?target=' + str(target)
    
class Session(db.Model):
    user_id = db.StringProperty(required=True)
    valid_until = db.DateTimeProperty(required=True)

    @staticmethod
    def create_session_for_user(user_id):
        Session.delete_session_for_user(user_id)
        valid_until = datetime.datetime.now() + datetime.timedelta(seconds = 86400)
        s = Session(user_id = user_id, valid_until = valid_until)
        s.put()
        return s.key().id()

    @staticmethod
    def delete_session_for_user(user_id):
        db.delete(Session.all().filter('user_id =', user_id))

    @staticmethod
    def get_session(session_id):
        try:
            s = Session.get_by_id(long(session_id))
            if s and s.valid_until > datetime.datetime.now():
                return s
        except Exception, e:
            logging.error('Error while getting session: '+str(e))
        return None

class Course(db.Model):
    name = db.StringProperty(required=True)
    