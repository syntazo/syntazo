
from django.conf.urls.defaults import *

urlpatterns = patterns('hello.views',
#  (r'^$', 'index'),
  (r'^add_course$', 'add_course'),
  (r'^add_app$', 'add_app'),
  (r'^add_tournament_heat$', 'add_tournament_heat'),
  (r'^$', 'index'),
  (r'^/$', 'index'),
  (r'^/index.html$', 'index'),
  (r'^/index.php$', 'index'),
  (r'^edit_course/(?P<id>\d+)', 'edit_course'),
  (r'^edit_course', 'edit_course'),
  (r'^edit_app/(?P<id>\d+)', 'edit_app'),
  (r'^edit_app', 'edit_app'),
  (r'^edit_tournament_heat/(?P<id>\d+)', 'edit_tournament_heat'),
  #(r'^run_tournament', 'run_tournament'),
  (r'^run_tournament_heat/(?P<id>\d+)', 'run_tournament_heat'),
  (r'^live_run_tournament_heat/(?P<id>\d+)', 'live_run_tournament_heat'),
)