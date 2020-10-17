from flask import request,jsonify,render_template,abort
from flask_restful import Resource
from app import app
from settings import Config
from models.models import *
from utils.func import esn,obpasw,gecktoken
from datetime import datetime
import uuid

#Forums categories and Questions from this Categories
class Forum(Resource):
	def get(self,key):
		#if get key is equal all deduce all categories
		if 'all' in key:
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

		abort(404)

	def post(self,cate):
		if 'token' in request.get_json():

			data = request.get_json()

			if 'admin' in cate:
				print('ADMINS')

				adm = gecktoken(Config.SECRET_KEY,0,token=data['token'])
				print(adm)
				if adm != None and True is adm['is_staff']:
					db.session.add(Games(games=data['topic'],public_id=str(uuid.uuid4()))),db.session.commit()
					return jsonify({'message':'Category successfully create'})
				
				return jsonify({'message':'You have no proper rights for create Categoris '})
			
			elif 'users' in cate:
				usr = gecktoken(Config.SECRET_KEY,0,token=data['token'])
				if usr != None and Games.query.filter_by(public_id=data['cate']).first() != None:
					a = PlayerAnnouncements(public_id=str(uuid.uuid4()),topic=data['topic'],author=usr['login'],cate_id=data['cate_id'],body=data['body'])

					db.session.add(a),db.session.commit()
					return jsonify({'message':'Post is create'})

				return jsonify({'message':'this category is not or link is not valid'})
		
		abort(404)

	def put(self):
		pass

	def delete(self):
		pass

#message from this forum
class ForumPosts(Resource):
	#Output question and message for this questions
	def get(self,key):
		b,topi = PlayerAnnouncements.query.filter_by(public_id=key).first(),{}
		if b != None:
			topi['topic'] = [b.public_id,b.topic,b.author,b.pub_date,b.cate_id,b.post_rating]
			a = MessageForumUser.query.filter_by(post_id=key).all()
			if a != []:
				tt = datetime.now()
				
				mes = {'message' : [[i.user_name,i.message_user,i.send_date] for i in a]}
				topi['meslen'] = len(mes)
				
				print('Выгружено за ', datetime.now() - tt)
				
				return jsonify({'top':topi,'mes':mes})
			
			topi['meslen'] = 0
			return jsonify({'top':topi,'mes':mes})

		abort(404)

	#Users message
	def post(self):
		data = request.get_json()

		return jsonify({'message':'ok'})

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

	#Remove question for specific category
	def delete(self):
		pass
