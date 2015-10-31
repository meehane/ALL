import socket 
import threading
import os

def retrfile(name,sock):
	filename=sock.recv(1024)
	if os.path.isfile(filename):
		sock.send('EXISTS'+str(os.path.getsize(filename)))
		userresponse=sock.recv(1024)
		if userresponse[:2]=='ok':
			with open(filename,'rb') as f:
				bytestosend=f.read(1024)
				sock.send(bytestosend)
				while bytestosend!="":
					bytestosend=f.read(1024)
					sock.send(bytestosend)
	else:
		sock.send('file does not exist')
	sock.close()

def main():
	host=socket.gethostname()
	port=5000
	s=socket.socket()
	s.bind((host,port))
	s.listen(5)
	print('server started')
	while True:
		c,addr=s.accept()
		print('client connected to addr :->',addr)
		t=threading.Thread(target=retrfile,args=('retrthread',c))
		t.start()
	s.close()

if __name__=='__main__':
	main()
