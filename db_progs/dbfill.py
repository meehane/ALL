import shelve
import sys
import crypt


db = shelve.open('users')

uname = sys.argv[1]
passw = sys.argv[2]

passw = crypt.crypt(passw, crypt.METHOD_SHA512)

test = {'username':uname, 'password':passw}

db['test'] = test

db.close()
