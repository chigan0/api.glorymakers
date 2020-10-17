from flask import request,jsonify
from app import app
from settings import Config
from models.models import Users,db,Games,PlayerAnnouncements
from utils.func import esn,obpasw,gecktoken
import threading

def authorization():
	data = request.get_json()
	message = {'message':'Invalid Username or Password'}
	if 'email' in data and 'password' in data:
		se = Users.query.filter_by(email=data['email']).first()
		if se != None:
			hasp = obpasw(data['password'],Config.SECRET_KEY)
			message = {'message':'Invalid Password or Your mail has not been verified','status':'401'}
			if se.password_hash == hasp and se.confirmed == True and se.confirmed_pass == True:
				return jsonify(
					{
						'status':'200',
						'login':se.public_id,
						'token':gecktoken(
									Config.SECRET_KEY,
									1,
									public_id=se.public_id,
									email=se.email,
									login=se.login,
									password_hash=hasp,
									is_staff=se.is_staff,
									is_superuser=se.is_superuser,
									is_level=se.is_level,),
					}),200
		
	return jsonify(
			message
		)

def checktoken():
	if 'token' in request.get_json():
		data = request.get_json()
		res = gecktoken(Config.SECRET_KEY,0,token=data['token'])

		if res != False:
			a = Users.query.filter_by(public_id=res['public_id']).first()
			if a != None:
				return jsonify({
						'status':'200',
						"message":"This user is found"
					}),200
		
	return jsonify(
		{
			"status": '404',
			"message":"This user with an identical token was not found"
		})

def tees():
	print(request.get_json())
	return jsonify({'message':'Hello VueJS'})
