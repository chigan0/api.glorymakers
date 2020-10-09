from flask import request,jsonify
from app import app
from settings import Config
from models.models import Users,db,Games,PlayerAnnouncements
from utils.func import esn,obpasw,gecktoken

def authorization():
	data = request.form
	se = Users.query.filter_by(email=data['email']).first()
	message = {'message':'Invalid Username or Password'}
	if se != None:
		hasp = obpasw(data['password'],Config.SECRET_KEY)
		message = {'message':'Invalid Password or Your mail has not been verified','status':'401'}
		if se.password_hash == hasp and se.confirmed == True and se.confirmed_pass == True:
			return jsonify(
				{
					'status':'200',
					'login':se.public_id,
					'token':gecktoken(Config.SECRET_KEY,1,public_id=se.public_id,login=se.login,password_hash=hasp),
				}),200
	
	return jsonify(
			message
		)

def checktoken():
	print(request.get_json())
	data = request.form
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
			"status": '203',
			"message":"This user with an identical token was not found"
		}),203

@app.route('/v1/test/',methods=['POST','GET'])
def tees():
	print(request)
	return jsonify({'message':'dawdawda'})