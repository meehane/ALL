import sys, socket, select, time, base64, os, crypt, pickle, datetime
from pytz import timezone
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

#send message to all clients
def send_message(sock, message):
	for socket in clients:
		if socket != connect_socket and socket != sock: #Don't send the client their own messages
			try:
				if socket in keys:
					cipher = AES.new(keys[socket])
					message1 = encrypt_aes(cipher,message)
				socket.send(message1)
			except: #broken connection
				socket.close()
				del keys[socket]
				clients.remove(socket)

def send_single_message(socket, message):
	print("SENDING SINGLE MESSAGE")
	try:
		if socket in keys:
			cipher = AES.new(keys[socket])
			message1 = encrypt_aes(cipher,message)
		socket.send(message)
	except:
		socket.close()
		del keys[socket]
		clients.remove(socket)

#decrypt RSA
def decrypt_rsa(key):
	private_key = RSA.importKey(open("priv.pem","r"))
	return(private_key.decrypt(key))

#decrypt/encrypt AES functions
def pad_for_enc(message):
	return(message +(32 - len(message) % 32) * "{")

def encrypt_aes(cipher, message):
	return(base64.b64encode(cipher.encrypt(pad_for_enc(message))))

def decrypt_aes(cipher, encrypted):
	return(cipher.decrypt(base64.b64decode(encrypted)).rstrip("{"))
#Get current time
def current_time():
	current_time = datetime.datetime.now(timezone('UTC')
	#hours = current_time.strftime("%l")
	#minutes = current_time.minute
	time = current_time.strftime("%H:%M:%S")
	#return(str(hours) + ":"  + str(minutes) + ampm)
	return(time)

#list of clients sockets
clients = []
#dictionary of client's AES keys
keys = {}
#dictionary of clients usernames
usernames = {}

port = 80
host = ""

connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connect_socket.bind((host,port))
connect_socket.listen(10)

clients.append(connect_socket)

print "Chat server started on port " + str(port)

while True:

	read, write, error = select.select(clients,[],[])

	for socket in read:		
		#START HANDLE NEW CONNECTION
		if socket == connect_socket:
			sock, address = connect_socket.accept()
			clients.append(sock)
			print "New connection from " + str(address)
		#END HANDLE NEW CONNECTION
		else:
			try:
				#RECEIVE MESSAGE FROM CLIENT
				message = socket.recv(4096)
				if message:
					if message[0:9] == "setnewkey":
						#set aes key for client
						aes_key = tuple({message[9:]})
						aes_key = str(decrypt_rsa(aes_key))
						if socket not in keys:
							keys[socket] = aes_key
					else:
						#decrypt message
						cipher = AES.new(keys[socket])
						message = decrypt_aes(cipher,message)
						
						if message[0:8] == "setname ":
							#START OF AUTH
							file = open('users.db', 'rb')#open a database of authenticated users
							db = pickle.load(file)
							user = message[8:]
							username,password = user.split(",")
							login_success = "false" #initially the user is not authenticated
							for key,item in db.items():
								if key == username.decode("ascii"):#search the database for the entered username
									comp_hash = item #get the users stored password hash
									hash = crypt.crypt( password.decode("ascii"), comp_hash)#hash the entered username with the stored password
									if comp_hash == hash:#if they match
										login_success = "true"#set the authenticated value to true
							file.close()
							if login_success == "true" :
								usernames[socket] = username
							else:
								socket.close()
							#END OF AUTH
							while len(keys[socket]) < 32:
								time.sleep(0.1)
							send_message(connect_socket, "\r<Server> " + usernames[socket] + " has entered the chat!\n")
						else:
							#broadcast message
							send_message(socket, "\r" +"<" + usernames[socket] + "> [" + current_time() + "] " + message)
				#END RECEIVE MESSAGE FROM CLIENT
			except:
				#if it cant rcv on socket, client must have disconnected
				try:
					send_message(socket, "%s has disconnected" % usernames[socket])
					print "%s has disconnected" % usernames[socket]
					socket.close()
					clients.remove(socket)
					del keys[socket]
					continue
				except:
					socket.close()
					clients.remove(socket)#send_message(connect_socket, "Someone has disconnected")
					continue
connect_socket.close()
