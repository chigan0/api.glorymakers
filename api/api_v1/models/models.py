from app import db
from settings import Config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

class Users(db.Model):
	__tablename__='user'
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	public_id = db.Column(db.String,unique=True)
	email = db.Column(db.String(120),unique=True,nullable=False)
	login = db.Column(db.String(120),unique=True,nullable=False)
	password_hash = db.Column(db.String(356),nullable=False)
	is_staff = db.Column(db.Boolean,default=False)
	is_superuser = db.Column(db.Boolean,default=False)
	is_level = db.Column(db.Integer,default=False)
	confirmed = db.Column(db.Boolean, default=False)
	confirmed_pass = db.Column(db.Boolean,default=True)
	create_date = db.Column(db.String, default=datetime.utcnow())

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(Config.SECRET_KEY,expiration)
		return s.dumps({'confirm':self.id}).decode('utf-8')

	@staticmethod
	def set_password(login,email,password_hash,new_pass):
		a = Users.query.filter_by(login=login).first()
		if a.password_hash == password_hash:
			a.password_hash,a.email = new_pass,email
			db.session.add(a),db.session.commit()
			return True
		return False

	@staticmethod
	def confirm(token,check):
		s = Serializer(Config.SECRET_KEY)
		try:
			data = s.loads(token)
		except:
			return False
			
		a = Users.query.get(data['confirm'])
		if a != None:
			if check == 0:
				if a.confirmed == False:
					a.confirmed = True
					db.session.add(a),db.session.commit()
					return a
			elif check == 1:
				if a.confirmed == True and a.confirmed_pass == False:
					return a
		return False

	def __repr__(self):
		return '<User email %r>' % self.email

class Games(db.Model):
	__tablename__='games'
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	games = db.Column(db.String(64),nullable=False,unique=True)
	public_id = db.Column(db.String,unique=True)
	create_date = db.Column(db.String,default=datetime.utcnow())
	cate = db.relationship('PlayerAnnouncements',backref='cate_name',lazy='dynamic')

	def __repr__(self):
		return 'Games %r' % self.games

class PlayerAnnouncements(db.Model):
	__tablename__='announcements'
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	public_id = db.Column(db.String,unique=True)
	topic = db.Column(db.String(64),unique=True,nullable=False)
	author = db.Column(db.String(54),default='автор не указан')
	body = db.Column(db.String(5000),default='отсутствует')
	pub_date = db.Column(db.String,default=datetime.utcnow())
	cate_id = db.Column(db.String, db.ForeignKey('games.public_id'))
	mess = db.relationship('MessageForumUser',backref='forum_mes',lazy='dynamic')
	post_rating = db.Column(db.Integer,default=0)

	def __repr__(self):
		return 'Topic %r' % self.topic

class MessageUser(db.Model):
	__tablename__='message_user'
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	body = db.Column(db.String(512))


class MessageForumUser(db.Model):
	__tablename__='mesage_forum'
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	user_name = db.Column(db.String(120),nullable=False,default='Анонимно')
	message_user = db.Column(db.String(568))
	post_id = db.Column(db.String,db.ForeignKey('announcements.public_id'))
	send_date = db.Column(db.String,default=datetime.utcnow())


class PostRaiting(db.Model):
	id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
	post_id = db.Column(db.String,db.ForeignKey('announcements.public_id'))
	user_like = db.Column(db.String(120),nullable=False,default='Анонимно')

class OnlineUsers(db.Model):
	__bind_key__='usersstat'
	id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
	user_name = db.Column(db.String(120))