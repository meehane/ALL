import shelve

print ("opening database")

db = shelve.open('users')

print ('Database open')

print ('reading test')

print (db['test'])

print ('printing passwords')

for key in db:
		print (db[key])