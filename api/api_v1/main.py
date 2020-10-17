#This file describes is routers of this api

from app import app,api,socketio,got_request_exception
from views import *
from resources.users import *
from resources.forums import *
from resources.chats import *
from utils.func import log_exception

'''
Url /v1/authorization/ for authorizations,
Url /v1/token/check/ for check token,
Url /v1/test/ for test connect to api,

Class Logan is for user registrations,email confirmed and change password,
Class RestorPassword is for restor user is password,
Class Forum is output categories and questions this category,
Class ForumPost  output user's message this questions,
socketio Connects 
'''

app.add_url_rule('/v1/authorization/',view_func=authorization,methods=['POST'])
app.add_url_rule('/v1/token/check/',view_func=checktoken,methods=['POST'])
app.add_url_rule('/v1/test/',view_func=tees,methods=['GET','POST','PUT','DELETE'])

api.add_resource(Logan,'/v1/login/','/v1/login/<public_id>','/v1/login/confirm/<token>')
api.add_resource(RestorPassword,'/v1/login/restore_password/<token>/','/v1/login/restore_password/')
api.add_resource(Forum,'/v1/get/<key>/','/v1/add/<cate>/')
api.add_resource(ForumPosts,'/v1/get/public_id/<key>/','/v1/put/public_id/')

socketio.on_namespace(Chat('/v1/chats/'))

got_request_exception.connect(log_exception, app)

if __name__ == '__main__':
	socketio.run(app)