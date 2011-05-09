
from django.conf.urls.defaults import *

urlpatterns = patterns('hello.views',
#  (r'^$', 'index'),
  (r'^add_course$', 'add_course'),
  (r'^add_app$', 'add_app'),
  (r'^$', 'index'),
  (r'^/$', 'index'),
  (r'^/index.html$', 'index'),
  (r'^/index.php$', 'index'),
  (r'^edit_course/(?P<id>\d+)', 'edit_course'),
  (r'^edit_course', 'edit_course'),
  (r'^edit_app/(?P<id>\d+)', 'edit_app'),
  (r'^edit_app', 'edit_app'),
  (r'^run_tournament', 'run_tournament'),
)