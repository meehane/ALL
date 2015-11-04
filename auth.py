import crypt
import socket
import pickle

def authenticate (sock):
	"""This function takes a socket as input and produces a bool as output"""
	
	username = raw_input("username: ")
	password = raw_input ("Please enter a password ")
	
	while True:#make sure there are no commas in the username or password
		if ',' in username:#the server will break oherwise
			username  = raw_input("Error: please pick a user without commas")
		elif ',' in password:
			password = raw_input("Error: please use a password without commas")
		else:
			break
	#print (password + '\n\n\n\n') #intermediate print this will be removed later

	data = username + ',' + password
	
	#print (data)#another intermediate print
	
	sock.send(data.encode("ascii"))#send to the server for comparison
	auth = sock.recv(1024)#will recieve a bool back
	if auth.decode("ascii") == "True":#if the passwords match
	
		print ("Hello", username, "you can start chating now")
		return True
	
	else:#if they don't
	
		print ("The username or password entered was incorrect. GTFO")
		return False

def server_auth(sock):	
	"""This is the server side counter part to the previous function it takes the connecing socket as input and sends a bool to the client"""

	file = open('users.db', 'rb')#open a database of authenticated users
	db = pickle.load(file)
	user = sock.recv(2048)#listen for the users hash
	#print ("recieved password hash from user")
	
	username,password = user.split(b',')#split the users concatenated data
					    #into username and password again
	for key, item in db.items():
		#print ("searching database")	
		#print (key)
		if key == username.decode("ascii"):#search the database for the username
			#print ("Searching for user")
			comp_hash = item #load the users stored password hash into memory
			
			hash = crypt.crypt( password.decode("ascii"), comp_hash)#hash the plain text file with the stored password
			#print ("comparing hashes")
			if comp_hash == hash:#if they match
				file.close()
				sock.send("True".encode("ascii"))#send a True signal to the client
				#print ("Hash matches")
			else:#other wise send a false signal
				file.close()
				#print ("hash doesn't match")
				sock.send("False".encode("ascii"))
		else:
			file.close()
			sock.send("False".encode("ascii"))
