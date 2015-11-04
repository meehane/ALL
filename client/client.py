import socket, select, string, sys, time, base64, os, crypt, pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

def prompt() :
	sys.stdout.write('<' + username + '> ')
	sys.stdout.flush()

def pad_for_enc(message):
	return(message +(32 - len(message) % 32) * "{")

def encrypt_aes(cipher, message):
	return(base64.b64encode(cipher.encrypt(pad_for_enc(message))))

def decrypt_aes(cipher, encrypted):
	return(cipher.decrypt(base64.b64decode(encrypted)).rstrip("{"))


#DYNAMIC PORT/IP START     
if(len(sys.argv) < 3) :
	print 'Usage : python client.py hostname port'
	sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
#DYNAMIC PORT/IP END

#STATIC PORT IP START
#host = 192.168.0.2
#port = 5000
#STATIC PORT/IP END

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(2)

#Make initial connection to server
try :
	s.connect((host, port))
except :
	print 'Unable to connect'
	sys.exit()


#generate AES key
aes_key = os.urandom(32)
public_rsa = RSA.importKey(open("pub.pem", "r"))
encrypted_aes = public_rsa.encrypt(aes_key,32)
cipher = AES.new(aes_key)

#Send AES key to server
s.send("setnewkey" + str(encrypted_aes[0]))

#START LOGIN
username = raw_input("Enter your username: ")
password = raw_input("Enter your password: ")

login_data = username + ',' + password

print 'Logging in to server...'
time.sleep(1)
s.send(encrypt_aes(cipher, "setname " + login_data))
#END LOGIN
message_count = 0
while 1:
	socket_list = [sys.stdin, s]
	#Get the list of sockets that are readable
	read, write, error = select.select(socket_list , [], [])
     
	for sock in read:
		#incoming message from remote server
		if sock == s:
			data = sock.recv(4096)
			if not data:
				if message_count == 0 :
					print("Login failed.")
				print "\nDisconnected from chat server."
				sys.exit()
			else:
				#print data
				data = decrypt_aes(cipher, data)
				sys.stdout.write(data)
				prompt()
				message_count = message_count + 1        
		#user entered a message
        	else:
			message = sys.stdin.readline()
			#encrypt message
			message = encrypt_aes(cipher, message)
			s.send(message)
			prompt()
