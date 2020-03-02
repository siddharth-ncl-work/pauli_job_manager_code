import os
import time
import job_status
import submit_job
from subprocess import Popen

class job:

  def __init__(self,job_dir_path,job_type):
    self.job_dir_path=job_dir_path
    self.job_type=job_type
    self.ppid=None

  def submit(self):
    ppid=submit_job.submitJob(self)
    self.ppid=ppid

  def status(self):
    _job_status=job_status.jobStatus(self)
    return _job_status

  def removeFiles(self):
    if self.job_type=='opt':
      files_not_be_deleted='input'
      all_files=os.listdir(self.job_dir_path)
      for file in files_not_be_deleted.split():
        if file in all_files:
          all_files.remove(file)
      files_to_be_deleted=' '.join(all_files)
      print 'Deleting files: '+files_to_be_deleted
      p=Popen('rm -rf '+files_to_be_deleted,cwd=self.job_dir_path,shell=True)
      p.communicate()
    elif self.job_type=='numforce':
      print 'Deleting files: numforce NumForce.out vib*'
      p=Popen('rm -rf numforce NumForce.out vib*',cwd=self.job_dir_path,shell=True)
      p.communicate()
      #time.sleep(2)
    else:
      print 'job type %s does not exist, cannot remove files'%self.job_type

  def __str__(self):
    s='***JOB DESCRIPTION***\n'
    s+='Job Directory:'+self.job_dir_path+'\n'
    s+='Job Type:'+self.job_type
    if self.ppid!=None:
      s+='\nJob ppid:'+str(self.ppid)+'\n'
      s+='Job Status:'+self.status()
    return s
