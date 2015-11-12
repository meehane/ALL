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
				if socket in usernames:
					socket.send(message1)
			except: #broken connection
				socket.close()
        			if socket in keys:
					del keys[socket]
				print(str(socket) + " disconnected")
				#print clients
				if socket in clients:
					clients.remove(socket)
				time.sleep(1)
				send_message("<Server> " + str(users[socket]) + " has disconnected.")
				continue

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
		#print clients
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
	current_time = datetime.datetime.now(timezone('UTC'))
	time = current_time.strftime("%H:%M:%S")
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
loops = 0
while True:
	try:
		read, write, error = select.select(clients,[],[])
	except:
		if len(clients) > 0:
			clients.pop()
		continue
#	loops = loops + 1
#	if (loops % 20) == 0:
#		send_message(connect_socket,"ping")
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
								socket.send("wrng")
								clients.remove(socket)
								socket.shutdown()
								socket.close()
							#END OF AUTH
							while len(keys[socket]) < 32:
								time.sleep(0.1)
							send_message(connect_socket, "\r<Server> " + usernames[socket] + " has entered the chat!\n")
						else:
							#broadcast message
							send_message(connect_socket, "\r" +"<" + usernames[socket] + "> [" + current_time() + "] " + message)
				#END RECEIVE MESSAGE FROM CLIENT
			except:
				#if it cant rcv on socket, client must have disconnected
				try:
					send_message(socket, "\r<Server> %s has disconnected\n" % usernames[socket])
					print "%s has disconnected" % usernames[socket]
				except:
					print "Someone disconnected"
					
connect_socket.close()
