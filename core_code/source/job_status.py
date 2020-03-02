import os
import time
import subprocess
from subprocess import Popen,PIPE

def ppidFlag(ppid):
  p=subprocess.Popen(['ps','--ppid',str(ppid)],stdout=PIPE)
  output=(p.communicate()[0]).split('\n')
  if len(output)>2:
    return 'EXISTS'
  else:
    return 'BLANK'

def jobStatus(job):
  if job.job_type=='opt':
    return jobStatusOpt(job)
  elif job.job_type=='numforce':
    return jobStatusNumforce(job)

def searchDirFlagOpt(search_dir_path):
  search_dir_flag='NONE'
  for file in os.listdir(search_dir_path):
    if 'GEO_OPT_'in file:
      search_dir_flag=file.split('_')[-1]
      break
  return search_dir_flag
 
def jobStatusOpt(job):
  job_status=None
  search_dir_flag=None
  ppid_status=None
  search_dir_flag=searchDirFlagOpt(job.job_dir_path)
  ppid_flag=ppidFlag(job.ppid)
  if search_dir_flag.upper()=='CONVERGED':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
       job_status='DEAD'
  elif search_dir_flag.upper()=='FAILED':
    files=os.listdir(job.job_dir_path)
    if 'stop' not in files:
      print 'STOPPING OPT'
      Popen('touch stop',cwd=job.job_dir_path,shell=True).communicate()
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      job_status='DEAD'
  elif search_dir_flag.upper()=='RUNNING':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      print '[%d,%s,%s]: %s,%s,confirming..'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag)
      time.sleep(5)
      ppid_flag=ppidFlag(job.ppid)
      search_dir_flag=searchDirFlagOpt(job.job_dir_path)
      if ppid_flag=='EXISTS':
        job_status='ALIVE'
      elif ppid_flag=='BLANK':
        job_status='DEAD'
  elif search_dir_flag.upper()=='NONE':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      print '[%d,%s,%s]: %s,%s,confirming..'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag)
      time.sleep(5)
      ppid_flag=ppidFlag(job.ppid)
      search_dir_flag=searchDirFlagOpt(job.job_dir_path)
      if ppid_flag=='EXISTS':
        job_status='ALIVE'
      elif ppid_flag=='BLANK':
        job_status='DEAD'
  print '[%d,%s,%s]: %s,%s,%s'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag,job_status)
  return job_status

def searchDirFlagNumforce(search_dir_path):
  search_dir_flag='NONE'
  search_dir_opt_flag=searchDirFlagOpt(search_dir_path)
  if search_dir_opt_flag!='CONVERGED':
    return 'ERROR'
  if 'NumForce.out' not in os.listdir(search_dir_path):
    return 'NONE'
  file=open(search_dir_path+'/NumForce.out','r')
  lines=file.read()
  file.close()
  if 'END of NumForce'.lower() in lines.lower():
    search_dir_flag='PRESENT'
  else:
    search_dir_flag='ABSENT'
  return search_dir_flag

def jobStatusNumforce(job):
  job_status=None
  search_dir_flag=None
  ppid_status=None
  search_dir_flag=searchDirFlagNumforce(job.job_dir_path)
  ppid_flag=ppidFlag(job.ppid)
  if search_dir_flag=='PRESENT':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
       job_status='DEAD'
  elif search_dir_flag=='ABSENT':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      print '[%d,%s,%s]: %s,%s,confirming..'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag)
      time.sleep(5)
      ppid_flag=ppidFlag(job.ppid)
      search_dir_flag=searchDirFlagNumforce(job.job_dir_path)
      if ppid_flag=='EXISTS':
        job_status='ALIVE'
      elif ppid_flag=='BLANK':
        job_status='DEAD'
  elif search_dir_flag=='ERROR':
    files=os.listdir(job.job_dir_path)
    if 'numforce' in files:
      print 'STOPPING NUMFORCE...'
      Popen('touch numforce/stop',cwd=job.job_dir_path,shell=True).communicate()
    elif ppid_flag=='EXISTS' and 'numforce' not in files:
      print 'ERROR: Cannot stop this numforce job'
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      job_status='DEAD'
  elif search_dir_flag=='NONE':
    if ppid_flag=='EXISTS':
      job_status='ALIVE'
    elif ppid_flag=='BLANK':
      print '[%d,%s,%s]: %s,%s,confirming..'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag)
      time.sleep(5)
      ppid_flag=ppidFlag(job.ppid)
      search_dir_flag=searchDirFlagNumforce(job.job_dir_path)
      if ppid_flag=='EXISTS':
        job_status='ALIVE'
      elif ppid_flag=='BLANK':
        job_status='DEAD'
  print '[%d,%s,%s]: %s,%s,%s'%(job.ppid,job.job_type,job.job_dir_path,search_dir_flag,ppid_flag,job_status)
  return job_status
