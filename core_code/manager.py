import os
import sys
import time
from subprocess import Popen,PIPE

from source import job_class
from source import wait

def make_pid_file():
  output_dir_path='..'
  curr_pid=os.getpid()
  print 'MANAGER PID: '+str(curr_pid)
  Popen('rm %s/*.pid'%output_dir_path,shell=True).communicate()
  Popen('touch %s/%d.pid'%(output_dir_path,curr_pid),shell=True).communicate()

def _keep_running(job):
  if job.job_type=='opt':
    Popen('mkdir input',cwd=job.job_dir_path,shell=True).communicate()
    Popen('cp * input',cwd=job.job_dir_path,shell=True).communicate()
  while True:
    print 'RUNNING JOB...\n'+str(job)
    job.removeFiles()
    if job.job_type=='opt':
      Popen('cp input/* .',cwd=job.job_dir_path,shell=True).communicate()
    job.submit()
    wait.wait(job)
    print str(job)+'\nJOB FINISHED\n'+'#'*80+'\n'

def run_jobs(keep_running,job_list,job_type_list):
  for i,job_dir_path in enumerate(job_list):
    job_type=job_type_list[i]
    curr_job=job_class.job(job_dir_path,job_type)
    if keep_running=='yes' and i==len(job_list)-1:
      _keep_running(curr_job)
    else:
      print 'RUNNING JOB...\n'+str(curr_job)
      curr_job.submit()
      wait.wait(curr_job)
      print str(curr_job)+'\nJOB FINISHED\n'+'#'*80+'\n'

def get_sys_agrs():
  keep_running=sys.argv[1]
  job_count=int(sys.argv[2])
  job_list=sys.argv[3:3+job_count]
  job_type_list=sys.argv[3+job_count:]
  args_dict={'keep_running':keep_running,'job_list':job_list,'job_type_list':job_type_list}
  return args_dict

def _run_jobs():
  interval=1
  while True:
    time.sleep(interval)

make_pid_file()
args_dict=get_sys_agrs()
print args_dict
print '#'*80
run_jobs(args_dict['keep_running'],args_dict['job_list'],args_dict['job_type_list'])
print 'MANAGER FINISHED!'
