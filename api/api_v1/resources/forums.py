from flask import request,jsonify,render_template
from flask_restful import Resource
from app import app
from settings import Config
from models.models import *
from utils.func import esn,obpasw,gecktoken
from datetime import datetime

#Forums categories and Questions from this Categories
class Forum(Resource):
	def get(self,key):
		#if get key is equal all deduce all categories
		if key == 'all':
			res = {}
			a = Games.query.all()
			for i in a:
				res[i.public_id] = i.games
			return jsonify(res=res)
		
		#if we get key from this category we will output this category
		elif key != 'all':
			a = Games.query.filter_by(public_id=key).first()
			if a != None:
				tim = datetime.now()
				res,ca = {},PlayerAnnouncements.query.filter_by(cate_id=a.public_id).all()
				for i in ca:
					res[i.public_id] = [i.topic,i.pub_date,a.games] 
				
				print(len(res), 'обектов выгружено за ', datetime.now() - tim)
				return jsonify({'res':res})

		return jsonify(message=key)

	def post(self,key):
		#при сравнении исползуй lower или upper
		data=request.get_json()
		if 'token' in data:
			a = gecktoken(Config.SECRET_KEY,0,token=data['token'])
			if a != False:
				return jsonify({'message':'Creating Successful'})

		return jsonify({'message':'You do not have permission to create a category'})

#message from this forum
class ForumPosts(Resource):
	#Output question and message for this questions
	def get(self,key):
		b,topi = PlayerAnnouncements.query.filter_by(public_id=key).first(),{}
		a,mes = MessageForumUser.query.filter_by(post_id=key).first(),{}
		if a != None:
			topi['topic'] = [b.public_id,b.topic,b.author,b.pub_date,b.cate_id,b.post_rating]
			mes['message'] = [a.user_name,a.message_user,a.send_date]
			return jsonify({'mes':mes,'top':topi})

		return jsonify({'message':'This is problem is closed'})

	def post(self):
		pass

	#Rating for this question from users
	def put(self):
		data = request.get_json()
		a=PlayerAnnouncements.query.filter_by(public_id=data['pub_id_room']).first()
		if a != None:
			us = gecktoken(Config.SECRET_KEY,0,token=data['token'])
			b = PostRaiting.query.filter_by(user_like=us['login']).first()
			print(b)
			if b == None:
				bb = PostRaiting(post_id=data['pub_id_room'],user_like=us['login'])
				a.post_rating += data['num']
				db.session.add(bb)
				db.session.add(a)
				db.session.commit()
				
				return jsonify({'status':'True'})