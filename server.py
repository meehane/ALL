import socket, select, time, base64, os
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


#list of clients
clients = []
#dictionary of client's AES keys
keys = {}
#dictionary of clients usernames
usernames = {}
#dict of ciphers
#cipher = {}

port = 5000
host = socket.gethostname()

connect_socket = socket.socket()
connect_socket.bind((host,port))
connect_socket.listen(10)

clients.append(connect_socket)

print "Chat server started on port " + str(port)

announce_time = 5 #number of seconds between client announcements
last_announce = 0

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
							usernames[socket] = message[8:]
							while len(keys[socket]) < 32:
								time.sleep(0.1)
							send_message(connect_socket, "\r<Server> " + usernames[socket] + " has entered the chat!\n")
						else:
							#broadcast message
							send_message(socket, "\r" +"<" + usernames[socket] + "> " + message)
							#print "\r<" + usernames[socket] + "> " + message
				#END RECEIVE MESSAGE FROM CLIENT
			except:
				#if it cant rcv on socket, client must have disconnected
				send_message(socket, "%s has disconnected" % usernames[socket])
				print "%s has disconnected" % usernames[socket]
				socket.close()
				clients.remove(socket)
				del keys[socket]
				continue

connect_socket.close()
