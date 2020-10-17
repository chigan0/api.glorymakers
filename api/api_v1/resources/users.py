from flask import request,jsonify,render_template
from flask_restful import Resource
from app import app
from settings import Config
from models.models import Users,db
from utils.func import esn,obpasw,gecktoken
import uuid


class Logan(Resource):
	def get(self,token):
		me = Users.confirm(token,0)
		if me != False:
			return jsonify({'token':gecktoken(Config.SECRET_KEY,1,public_id=me.public_id,login=me.login,password_hash=me.password_hash)})
		
		return jsonify({'message':'The user has already confirmed his mail and can log in'})

	def post(self):
		data = request.get_json()
		gen_hassh = obpasw(data['password'],Config.SECRET_KEY)
		
		if Users.query.filter_by(email=data['email']).first() == None:
			new_user = Users(public_id=str(uuid.uuid4()),email=data['email'],login=data['login'],password_hash=gen_hassh)
			
			db.session.add(new_user)
			db.session.commit()
			token = new_user.generate_confirmation_token()

			print(new_user.public_id)

			db.session.rollback()
			
			esn(render_template,app,text='Confirm Your Email',name=data['login'],email=data['email'],token=token,url='http://127.0.0.1:5000/v1/login/confirm/')
			
			return {"message":'Confirm your email to complete registration'},200
		
		return {"message":'User with identical mail is already registered'},203

	def put(self):
		data = request.get_json()

		password_old,password_new = obpasw(data['password_old'],Config.SECRET_KEY),obpasw(data['password_new'],Config.SECRET_KEY)
		res = Users.set_password(data['login'],data['email'],password_old,password_new)

		if res == True:
			return jsonify({"message":"succesfull"})
		
		return jsonify({"message":"noooooooooooooooo"})
	
	def delete(self,public_id):
		data = request.get_json()
		if 'token' in data:
			user = Users.query.filter_by(public_id=public_id).delete()
			db.session.commit()
			return jsonify({"message":"User is deleted"}),200
		return jsonify({'message':'This user is and password_hash not match'})

class RestorPassword(Resource):
	passver = {}
	
	def post(self):
		if request.get_json():
			data = request.get_json()
			re = Users.query.filter_by(email=data['email']).first()

			#re.login == data['login']
			print(re.confirmed)

			if re != None and re.confirmed == True:
				
				self.passver[re.id],re.confirmed_pass = obpasw(data['password'],Config.SECRET_KEY),False
				db.session.add(re),db.session.commit()
				token = re.generate_confirmation_token()
				esn(render_template,app,text='Confirm Your Email',name=re.login,email=data['email'],token=token,url='http://127.0.0.1:5000/v1/login/restore_password/')
				
				return jsonify({'message':'confrim your email'})

		return jsonify({'message':'This user is not defined'})

	def get(self,token):
		re = Users.confirm(token,1)
		print(re)
		if re != False:
			re.password_hash,re.confirmed_pass = self.passver[re.id],True
			db.session.add(re),db.session.commit()
			self.passver.pop(re.id)
			return jsonify({'token':gecktoken(Config.SECRET_KEY,1,public_id=re.public_id,login=re.login,password_hash=re.password_hash)})

		return jsonify({'message':'The user has already confirmed his mail and can log in'})
