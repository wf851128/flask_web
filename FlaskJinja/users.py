from flask import Blueprint, render_template, abort,jsonify,make_response,request,url_for,g
from functools import wraps
from jinja2 import TemplateNotFound
from FlaskJinja import auth,db
from . import model1
import json
import redis


mod = Blueprint('user', __name__,
                        template_folder='templates')

@mod.route('/user/home')
def home():
        return render_template(
        'user/500.html',
        title='Home'
    )

@mod.route('/user/task',methods=['POST'])
@auth.login_required
def task():
    return jsonify({'status': '0', 'url': 'home'})


@mod.route('/user/setting',methods=['POST'])
def setting():
    #r = redis.StrictRedis(host='192.168.2.114', port=6379, decode_responses=True,password='123456')
    # r = redis.StrictRedis(host='0.0.0.0', port=6379)
    # 如果要指定数据库，则 r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
    global rr
    rr.set('name', 'test')
    n=rr.get('name')
    return jsonify({'status': '0', 'url': n})

@mod.route('/user/register',methods=['POST'])
def register():
        abc = request.get_data()
        dict1 = json.loads(abc)
        username = dict1['username']
        password = dict1['password']
        if model1.User.query.filter_by(user_name = username).first() is not None:
            abort(400) # existing user
        user = model1.User(user_name = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'username': user.user_name })

@mod.route('/user/login',methods=['POST'])
def login():
        abc = request.get_data()
        dict1 = json.loads(abc)
        username = dict1['username']
        password = dict1['password']
        re = verify_password(username,password)
        if re:
            token = g.user.generate_auth_token()
            return jsonify({ 'result': 'OK','token': token.decode('ascii')})
        return jsonify({ 'result': re })

@auth.verify_token
def verify_token(token):
    print(token)
    user = model1.User.verify_auth_token(token)
    if user:
        g.current_user = user
        return True
    return False

def verify_password(username, password):
    user = model1.User.query.filter_by(user_name = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return user

