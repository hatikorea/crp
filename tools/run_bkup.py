import socket
import sys
import os
import subprocess as subp
import datetime
import time

#SETTING
TIME_CONTROL = True

os_env = dict(os.environ)
os_env['PATH'] = os_env['PATH']+':' + os.getcwd()
run_cmd = 'python3.4'


def get_ip():
	sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sk.settimeout(0)
	try:
		sk.connect(('10.255.255.255', 1))
		ip = sk.getsockname()[0]
	except Exception:
		ip = '127.0.0.1'
	finally:
		sk.close()
	return ip

if TIME_CONTROL:
	time_start = datetime.time(0, 0, 0, 0)     #00h00
	time_stop = datetime.time(23, 59, 0, 0)    #00h00
	time_now = datetime.datetime.now().time()
	while time_now < time_start:
		print('Waiting')
		time.sleep(60)
		time_now = datetime.datetime.now().time()

	run_process = subp.Popen([run_cmd, '--config', 'config.txt'], env=os_env)
	
	duration = ((time_stop.hour - time_now.hour)*60+(time_stop.minute-time_now.minute))*60

	try:
		run_process.communicate(timeout=duration)
	except:
		run_process.terminate()

else:
	dell_all = 0
	run_process = subp.Popen(run_cmd, env=os_env)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	server_ip = get_ip()
	server_port = 9208
	print('starting up on {} port {}'.format(server_ip, server_port))
	sock.bind((server_ip, server_port))

	# Listen for incoming connections
	sock.listen(1)

	server_listen = True
	while server_listen:
		# Wait for a connection
		print('waiting for a command ...')
		connection, client_address = sock.accept()
	
		try:
			print('connection from: ', client_address)
			# Receive the data in small chunks and retransmit it
			while True:
				data = connection.recv(16)
				mess_rcv = data.decode()
				if mess_rcv=='STATUS':
					if dell_all:
						mess_sent = 'STT-Deleted'
					else:
						run_status = run_process.poll()
						if run_status is None:
							mess_sent = 'STT-Runnig'
						else:
							mess_sent = 'STT-Killed'
				elif mess_rcv=='KILL-PROC':
					run_status = run_process.poll()
					if run_status is None:
						run_process.terminate()
						mess_sent = 'Proc-Killed'
					else:
						mess_sent = 'Not-Runing'
					print('received command: {}'.format(mess_rcv))

				elif mess_rcv=='RE-PROC':				
					if dell_all:
						mess_sent = 'Was-Deleted'
					else:
						run_status = run_process.poll()
						if run_status is None:
							mess_sent = 'Runnig'
						else:
							run_process = subp.Popen(run_cmd, env=os_env)
							mess_sent = 'Proc-Started'

				elif mess_rcv=='DEL-ALL':				
					if dell_all:
						mess_sent = 'Was-Deleted'
					else:
						run_status = run_process.poll()
						if run_status is None:
							run_process.terminate()
						os.system('rm -rf *')
						dell_all = 1
						mess_sent = 'All-Deleted'

				elif mess_rcv == 'TER-RESET':
					os.system('reset')
					mess_sent = 'Reseted'

				elif mess_rcv == 'END-SERVER':
					if dell_all:
						server_listen = False
					else:
						run_status = run_process.poll()
						if run_status is None:
							run_process.terminate()
						server_listen = False
						mess_sent = 'SERVER-Ended'

				else:
					mess_sent = 'Not-support: ' + mess_rcv
					run_status = run_process.poll()
					if run_status is None:
						run_process.terminate()
					os.system('reset')
					print('command is not clear: ', mess_rcv)
			
				connection.sendall(mess_sent.encode())
				break

		finally:
			# Clean up the connection
			connection.close()

	run_status = run_process.poll()
	if run_status is None:
		run_process.terminate()

os.system('reset')
print('End')


