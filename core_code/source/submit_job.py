import subprocess
from subprocess import Popen,PIPE
import shlex

def submitJob(job):
  if job.job_type=='opt':
    return submitOptJob(job)
  elif job.job_type=='numforce':
    return submitNumforceJob(job)
  else:
    print 'ERROR: job_type %s does not exists'%self.job_type

def modifyScript(script_file_path,job_dir_path):
  file=open(script_file_path,'r')
  data=file.readlines()
  file.close()
  for i,line in enumerate(data):
    if 'job_dir_path' in line:
      pos=i
      break
  data[pos]='job_dir_path=%s\n'%job_dir_path
  file=open(script_file_path,'w')
  file.write(''.join(data))
  file.close()

def submitOptJob(job):
  ppid=None
  modifyScript('scripts/opt_job_script.sh',job.job_dir_path)
  Popen('scripts/opt_job_script.sh',stdout=PIPE,stderr=PIPE)
  while ppid==None:
    p=Popen('ps aux|grep jobex',stdout=PIPE,shell=True)
    output=p.communicate()[0]
    for line in output.split('\n'):
      if 'jobex -ri -mfile file -c 2000' in line:
        ppid=int(line.split()[1].strip())
  print 'OPT JOB PPID: '+str(ppid)
  return ppid

def submitNumforceJob(job):
  ppid=None
  modifyScript('scripts/numforce_job_script.sh',job.job_dir_path)
  Popen('scripts/numforce_job_script.sh',stdout=PIPE,stderr=PIPE)
  while ppid==None:
    p=Popen('ps aux|grep NumForce',stdout=PIPE,shell=True)
    output=p.communicate()[0]
    for line in output.split('\n'):
      if 'NumForce -ri -mfile file' in line:
        ppid=int(line.split()[1].strip())
  print 'NUMFORCE JOB PPID: '+str(ppid)
  return ppid


  '''
  Popen('unset HOSTS_FILE',shell=True,executable='/bin/bash')
  Popen('export TURBODIR=/soft/vanka/TURBOMOLE/TURBOMOLE_6_4/TURBOMOLE',cwd=job.job_dir_path,shell=True,executable='/bin/bash')
  Popen('export PATH=$TURBODIR/scripts:$PATH',shell=True,executable='/bin/bash')
  Popen('export PARA_ARCH=MPI',shell=True,executable='/bin/bash')
  Popen('export PATH=$TURBODIR/bin/x86_64-unknown-linux-gnu/:$PATH',shell=True,executable='/bin/bash')
  Popen('export MPI_IC_ORDER="TCP"',shell=True,executable='/bin/bash')
  Popen('export PARNODES=12',shell=True,executable='/bin/bash')
  cmd=shlex.split('jobex -ri -mfile file -c 2000 > jobex.out &')
  p=Popen('jobex -ri -mfile file -c 2000 > jobex.out &',cwd=job.job_dir_path,shell=True,executable='/bin/bash')
  p.communicate()
  print 'submit '+str(p.pid)
  return p.pid
  '''
 
