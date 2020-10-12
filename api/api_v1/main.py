from app import app,api,socketio,got_request_exception
from views import *
from resources.users import *
from resources.forums import *
from resources.chats import *

app.add_url_rule('/v1/authorization/',view_func=authorization,methods=['POST'])
app.add_url_rule('/v1/token/check/',view_func=checktoken,methods=['GET','POST'])

api.add_resource(Logan,'/v1/login/','/v1/login/<public_id>','/v1/login/confirm/<token>')
api.add_resource(RestorPassword,'/v1/login/restore_password/<token>/','/v1/login/restore_password/')
api.add_resource(Forum,'/v1/get/<key>/','/v1/add/<cate>/')
api.add_resource(ForumPosts,'/v1/get/public_id/<key>/','/v1/put/public_id/')

socketio.on_namespace(Chat('/v1/chats/'))

got_request_exception.connect(log_exception, app)

if __name__ == '__main__':
	socketio.run(app)