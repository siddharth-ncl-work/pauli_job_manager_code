import time

def wait(job):
 interval=1
 stop_flag=False
 start_time=time.time()
 while not stop_flag:
   time.sleep(interval)
   job_status=job.status()
   if job_status=='ALIVE':
     stop_flag=False
   elif job_status=='DEAD':
     stop_flag=True
   elapsed_time=time.time()-start_time
   print '[%d,%s,%s]: waiting...%d seconds'%(job.ppid,job.job_type,job.job_dir_path,elapsed_time)
