import socket
import threading
import os

def main():
	host=raw_input('enter the ip address of the server')
	port=5000
	s=socket.socket()
	s.connect((host,port))
	filename=raw_input('enter the filename -> ')
	if filename!='q':
		s.send(filename)
		data=s.recv(1024)
		if data[:6]=="EXISTS":
			filesize=long(data[6:])
			message=raw_input('file exists'+str(filesize)+"bytes,download?(Y/N)-> ")
			if message=='Y' or message=='y':
				s.send('ok')
				f=open('new'+filename,'wb')
				data=s.recv(1024)
				totalrecv=len(data)
				f.write(data)
				while totalrecv<filesize:
					data=s.recv(1024)
					totalrecv+=len(data)
					f.write(data)
					print('{0:.2f}'.format((totalrecv/float(filesize))*100)+'%done')
				print('download complete')
		else:
			print('file does not exist')
	s.close()

if __name__=='__main__':
	main()

