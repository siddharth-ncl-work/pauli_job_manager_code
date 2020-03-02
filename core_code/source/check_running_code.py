import os
import sys
from subprocess import Popen,PIPE

arg=sys.argv[1]

if arg=='check':
  is_running=False
  process_name='manager.py'
  p1=Popen(['ps','aux'],stdout=PIPE)
  p2=Popen(['grep','python'],stdin=p1.stdout, stdout=PIPE)
  output=str(p2.communicate()[0]).split('\n')
  for line in output:
    if not line:
      continue
    prev_pid=int(line.split()[1].strip())
    if 'grep' not in line and process_name in line:
      is_running=True
  print is_running
elif arg=='info':
  process_name='manager.py'
  p1=Popen(['ps','aux'],stdout=PIPE)
  p2=Popen(['grep','python'],stdin=p1.stdout, stdout=PIPE)
  output=str(p2.communicate()[0]).split('\n')
  for line in output:
    if not line:
      continue
    prev_pid=int(line.split()[1].strip())
    if 'grep' not in line and process_name in line:
      print 'ERROR: previous manager code is running!!New code will not run!'
      print 'Previous running code pid: '+str(prev_pid)
