import pickle
import sys
import crypt

db = open('users.db', "rb")

uname = sys.argv[1]
passw = sys.argv[2]

passw = crypt.crypt(passw, crypt.METHOD_SHA512)

users = {}

users = pickle.load(db)
db.close()
db = open ('users.db', 'wb')
users [uname] = passw 

pickle.dump(users, db, protocol = 2)#this specifies pickle protocol two which is available in python 2.x

db.close()
