import crypt
import socket
import shelve

def authenticate (sock):
	"""This function takes a socket as input and produces a bool as output"""
	
	username = input("username: ")
	password = input ("Please enter a password ")

	print (password + '\n\n\n\n') #intermediate print this will be removed later

	data = username + ',' + password
	
	print (data)#another intermediate print
	
	sock.send(data.encode("ascii"))#send to the server for comparison
	auth = sock.recv(1024)#will recieve a bool back
	if auth.decode() == "True":#if the passwords match
	
		print ("Hello", username, "you can start chating now")
		return True
	
	else:#if they don't
	
		print ("The username or password entered was incorrect. GTFO")
		return False

def server_auth(sock):	
	"""This is the server side counter part to the previous function it takes the connecing socket as input and sends a bool to the client"""

	db = shelve.open('users')#open a database of authenticated users

	user = sock.recv(2048)#listen for the users hash
	print ("recieved password hash from user")
	
	username,password = user.split(b',')#split the users concatenated data
					    #into username and password again
	
	for key in db:
		
		if key == username.decode():#search the database for the username
			comp_hash = db[key]['password'] #load the users stored password hash into memory
			
			hash = crypt.crypt( password.decode(), comp_hash)#hash the plain text file with the stored password
			
			if comp_hash == hash:#if they match
			
				sock.send("True".encode("ascii"))#send a True signal to the client

			else:#other wise send a false signal
			
				sock.send("False".encode("ascii"))
		else:
			sock.send("False".encode("ascii"))
