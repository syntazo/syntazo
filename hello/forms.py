from django import forms
from google.appengine.ext.db import djangoforms
import models

#Use the default problemset if passed in

class CourseForm(djangoforms.ModelForm):
   class Meta:
     model = models.Course
     #exclude = ('interface', 'editor', 'isGamePath')
     
class AppForm(djangoforms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    class Meta:
        model = models.App
     #exclude = ('interface', 'editor', 'isGamePath')
