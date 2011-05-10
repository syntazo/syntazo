import os
import signal
import subprocess
import time
import urllib

PORT = 8080
APPNAME = '.'
SOURCE_DIRECTORIES= 'hello,tictactoe'

# To just launch the server without coverage
#coverage_proc = subprocess.Popen(['/usr/local/bin/dev_appserver.py', '.',
#							      '--clear_datastore',
#							      '--port=8080'])

coverage_proc = subprocess.Popen(['coverage',
								  'run',
								  '--source='+SOURCE_DIRECTORIES,
								  '/usr/local/bin/dev_appserver.py',
								  APPNAME,
								  '--clear_datastore',
								  '--port='+str(PORT),
								  '--use_sqlite'], 
#								  stdout=subprocess.PIPE,  #Comment out these lines to see stdout in console
#								  stderr=subprocess.STDOUT #Comment out these lines to see stdout in console
								  )
								  
print 'Waiting for server to launch'
time.sleep(2) #Give the server some time to boot up before fetching the index

data = ''
try: 
  print 'Fetching index'
  data = urllib.urlopen('http://localhost:8080').read() 
  print data
  
  print 'Fetching test data'
  data = urllib.urlopen('http://localhost:8080/test?format=plain').read() 
  print data

except ValueError:
  print '***** Handling the error *********'
  print ValueError

if 'FAILED' in data:
    print '*** Tests Failed ********************' 
    print '*** Not calculating coverage ********'

else:								  
  print '*** Creating html coverage report **'
  coverage_proc2 = subprocess.Popen(['coverage', 'html']) 

print '*** Killing dev_appserver process ***'
os.kill(coverage_proc.pid, signal.SIGINT)
print 'Exiting'
