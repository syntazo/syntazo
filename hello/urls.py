
from django.conf.urls.defaults import *

urlpatterns = patterns('hello.views',
#  (r'^$', 'index'),
  (r'^add_course$', 'add_course'),
  (r'^$', 'index'),
  (r'^/$', 'index'),
  (r'^/index.html$', 'index'),
  (r'^/index.php$', 'index'),

)