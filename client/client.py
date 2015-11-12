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
#if(len(sys.argv) < 3) :
	#print 'Usage : python client.py hostname port'
	#sys.exit()

#host = sys.argv[1]
#port = int(sys.argv[2])
#DYNAMIC PORT/IP END

#STATIC PORT IP START
host = "chat.teamudp.co.uk"
port = 80
#STATIC PORT/IP END

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(2)

#clear screen
####print '\x1b[1J'
os.system("clear")
print "\x1b[31m"
print "  _    _ _____  _____ \n | |  | |  __ \\|  __ \\\n | |  | | |  | | |__) |\n | |  | | |  | |  ___/ \n | |__| | |__| | |     \n  \\____/|_____/|_|\n\n"   




print '\x1b[32m',
#Make initial connection to server
try :
	s.connect((host, port))
	print'\rConnected to chat.teamudp.co.uk'
except :
	print 'Unable to connect to chat.teamudp.co.uk. Is the server running?'
	print '\x1b[37m'
	sys.exit()


#generate AES key
aes_key = os.urandom(32)
public_rsa = RSA.importKey(open("pub.pem", "r"))
encrypted_aes = public_rsa.encrypt(aes_key,32)
cipher = AES.new(aes_key)

#Send AES key to server
s.send("setnewkey" + str(encrypted_aes[0]))
try:
	#START LOGIN
	username = raw_input("Enter your username: ")
	password = raw_input("Enter your password: ")
except KeyboardInterrupt:
	print "\x1b[37m"
	sys.exit()

login_data = username + ',' + password

print 'Logging in to server...'
time.sleep(1)

s.send(encrypt_aes(cipher, "setname " + login_data))
#END LOGIN
time.sleep(1.5)
#clear screen
#####print '\x1b[1J'
os.system("clear")
message_count = 0
ping_count = 0
try:
	while 1:
		socket_list = [sys.stdin, s]
		#Get the list of sockets that are readable
		read, write, error = select.select(socket_list , [], [])
		#print(message_count)
		for sock in read:
			#incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data:
					#if message_count == 0 :
					#	print("Login failed.")
					s.close
					print "\nDisconnected from chat server."
					print '\x1b[37m'
					sys.exit()
				else:
					#print data
					if data[0:4] == "wrng":
						print '\x1b[31m',
						print "Login failed."
						print '\x1b[37m'
						sys.exit()
					#elif data[0:4] == "ping":
					#	ping_count = ping_count + 1
					else:
						data = decrypt_aes(cipher, data)
						sys.stdout.write(data)
						prompt()
						message_count = message_count + 1        
			#user entered a message
			else:
				message = sys.stdin.readline()
				message = message[:-1] + "                              \n"
				#encrypt message
				message = encrypt_aes(cipher, message)
				s.send(message)
				if message_count > 0:
					print('\x1b[1A\x1b[2K'),
				else:
					message_count = message_count + 1
				prompt()
except KeyboardInterrupt:	
	print '\x1b[37m'
	try:
		s.close()
	except:
		print "Socket not closed"
	sys.exit()		
