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
