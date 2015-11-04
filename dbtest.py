import pickle

print ("opening database")

db = open('users.db', 'rb')

#print ('Database open')

#print ('reading test')

#print (db['test'])

#print ('printing passwords')

users = pickle.load(db)
#print (users)

#for user in users:
#	print (users[user])
	#print (user
	#print (type(user))


for key, item in users.items():# this loops through the ditionaries keys
	print ("key: {0} password: {1}".format(key, item))#and prints the key along with the data
	if key == 'test':#this only prints the test data
		print (item)
