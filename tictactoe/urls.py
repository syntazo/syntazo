
from django.conf.urls.defaults import *

urlpatterns = patterns('tictactoe.views',
#  (r'^$', 'index'),
  (r'^$', 'index'),
  (r'^/$', 'index'),
  (r'^/index.html$', 'index'),
  (r'^/get_supported_games$', 'get_supported_games'),
  (r'^/get_new_board$', 'get_new_board'), 
  (r'^/is_board_valid$', 'is_board_valid'), 
  (r'^/is_move_valid$', 'is_move_valid'), 
  (r'^/get_next_move$', 'get_next_move'), 
  (r'^/game_status$', 'game_status'), 
 
)