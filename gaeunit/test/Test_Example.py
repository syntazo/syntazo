'''
Created on April 25, 2011

@author: Chris Boesch
'''
import unittest
#from google.appengine.ext import db
import logging
from hello import models

#import urllib
#import datetime
#from google.appengine.api import urlfetch
#from google.appengine.api import memcache
#from time import sleep
#from xxx import models
#from xxx import views

class Test_User(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        for x in models.User.all(): x.delete()
        
       
    def testUserCreation(self):  
        self.assertEqual(1, 1)
        user = models.User(user_id ='Bob').save()
        results = models.User.all()
        self.assertEqual(results.count(),1)
        
		
    def testUserCreation2(self):  
        self.assertEqual(1, 1)
        user = models.User(user_id ='Bob').save()
        results = models.User.all()
        self.assertEqual(results.count(),1)
		
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
