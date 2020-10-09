

'''
print(Configurations.SECRET_KEY)

secretKey = 'secret'

encoded_jwt = jwt.encode({'email': 'naz.abylai50@gmail.com','password_hash':'dwd3rfd2oih2yh97052fh3u'},secretKey, algorithm='HS256')

print(encoded_jwt)


print(jwt.decode(encoded_jwt,secretKey, algorithms=['HS256']))
'''
'''
import hashlib
import binascii

pas = 'rawdawdwa'

dk = hashlib.pbkdf2_hmac(hash_name='sha256',password=pas.encode('utf-8'),salt=Configurations.SECRET_KEY.encode('utf-8'),iterations=100000)
 
result = binascii.hexlify(dk)
 
print(result) 


import os

basedir=os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir))
'''
'''
a = 'dwadwdaw'
print('User email %r' % a)
'''

#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import sys

base_dir = os.path.abspath('../')
sys.path.append(base_dir)

from settings import *
from utils.func import *
#print(base_dir+'/settings.py')


#print(sys.path)


print(obpasw('gtx_-24071207',Config.SECRET_KEY))

ar = 5

ah = -1

print(ar+ah)

dwr = {'udarvedrom':'dwadawdawd'}



print('udarveddrom' in dwr)