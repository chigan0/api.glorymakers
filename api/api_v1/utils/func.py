def esn(render_template,app,**kwargs):
	from flask_mail import Mail,Message
	mail = Mail(app)
	
	msg = Message(kwargs['text'],sender='you@example.com',recipients=[kwargs['email']])
	msg.html = render_template('mail/email_temp.html',**kwargs)
	mail.send(msg)

def obpasw(password,SECRET_KEY):
	import hashlib
	import binascii

	dk = hashlib.pbkdf2_hmac(
		hash_name='sha256',
		password=password.encode('utf-8'),
		salt=SECRET_KEY.encode('utf-8'),
		iterations=100000
		)
	de = binascii.hexlify(dk)
	return de.decode('utf-8')

def gecktoken(secret_key,status,**kwargs):
	import jwt

	if status == 1:
		public_id,login,password_hash = kwargs['public_id'],kwargs['login'],kwargs['password_hash']
		token = jwt.encode({
			'public_id':public_id,
			'login':login,
			'password_hash':password_hash},
			secret_key,algorithm="HS256")

		return token.decode('utf-8')
	elif status == 0:
		try:
			res = jwt.decode(kwargs['token'],secret_key, algorithms=['HS256'])
			return res
		except:
			return False