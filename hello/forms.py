from django import forms
from google.appengine.ext.db import djangoforms
import models

#Use the default problemset if passed in

class CourseForm(djangoforms.ModelForm):
   class Meta:
     model = models.Course
     #exclude = ('interface', 'editor', 'isGamePath')
     
class AppForm(djangoforms.ModelForm):
   class Meta:
     model = models.App
     #exclude = ('interface', 'editor', 'isGamePath')
