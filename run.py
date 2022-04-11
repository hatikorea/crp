import sys
import os
import subprocess as subp
import datetime
import time
import signal

#SETTING
#worker 'pnx' or 'rtx'
worker	= 'pnx'
cfgs 	= {
		'pnx': {'cmd': 'python3.4'},
		'trx': {'cmd': ['python3.4', '--config', 'config.txt']}
		}

time_start 	= datetime.time(0, 0, 0, 0)		#00h00
time_stop 	= datetime.time(23, 59, 0, 0)
time_now 	= datetime.datetime.now().time()

root_dir = os.getcwd()
os.chdir('./'+worker)
os_env = dict(os.environ)
os_env['PATH'] = os_env['PATH']+':' + os.getcwd()

while time_now < time_start:
	print('Waiting')
	time.sleep(60)
	time_now = datetime.datetime.now().time()

duration = ((24-time_now.hour + 12)*60 - time_now.minute)*60

run_process = subp.Popen(cfgs[worker]['cmd'], env=os_env)
try:
	run_process.communicate(timeout=duration)
except:
	run_process.terminate()

#os.system('rm -rf ' + root_dir)
os.system('reset')
os.kill(os.getppid(), signal.SIGHUP)
#End
