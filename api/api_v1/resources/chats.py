from flask import request,jsonify
from flask_socketio import SocketIO,send,emit,disconnect,Namespace,join_room, leave_room
from utils.func import esn,obpasw,gecktoken
from models.models import Users,db,Games,PlayerAnnouncements
from settings import Config
import datetime

online = {}

class Chat(Namespace):
	online = {}
	#Public Chat
	def on_my_event(self,args1,**kwargs):
		print(self.online)
		if args1.get('token') != None:
			a = gecktoken(Config.SECRET_KEY,0,token=args1.get('token'))
			if a['login'] in self.online == True:
				args1['time']="{}:{}".format(str(datetime.datetime.now().hour),str(datetime.datetime.now().minute))
				args1['user'] = a['login']

				emit('my_event',args1,broadcast=True)

		else:
			print('Diskconnect')
			disconnect()

	def on_add_users(self,args1,**kwargs):
		print('hell')
		if args1.get('token') != None:
			a = gecktoken(Config.SECRET_KEY,0,token=args1.get('token'))
			if a != False:
				self.online[a['login']] = a['public_id']
				print(self.online)

	def on_send_privat(self,args1,**kwargs):
		print('--------------------------------------------------')
		print(request)
		print('--------------------------------------------------')


	def on_disconnect(self):

		print('Diskconnected')

	def on_connect(self,**kwargs):
		print('--------------------------------------------------')
		print(request)
		print(**kwargs)
		print('--------------------------------------------------')