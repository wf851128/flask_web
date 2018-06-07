from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
import redis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@192.168.2.114/flaskdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

CORS(app)
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Token')
from . import views,model1,users
app.register_blueprint(users.mod)
app.config['SECRET_KEY'] = 'OWKDJNJ3MASADNFO091U23JZ'  
pool = redis.ConnectionPool(host='192.168.2.114', port=6379)
rr = redis.StrictRedis(connection_pool=pool,password='123456')


# 登陆管理
# 声明login对象
login_manager = LoginManager()
# 初始化绑定到应用
login_manager.init_app(app)
# 声明默认视图函数为login，当我们进行@require_login时，如果没登陆会自动跳到该视图函数处理
login_manager.login_view = "login"

# 当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
from FlaskJinja import model1
@login_manager.user_loader
def load_user(userid):
    return model1.User.query.get(int(userid))

