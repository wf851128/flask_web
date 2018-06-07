from FlaskJinja import  db,app
from flask_login import  UserMixin
from passlib import apps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

#角色
class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref = 'role')


    def __repr__(self):
        return '<Role %r>' % self.role_name

#定义模型 Flask-SQLALchemy使用继承至db.Model的类来定义模型,如:
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    #每个属性定义一个字段
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),unique=True)
    pass_word = db.Column(db.String(200))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    #构造函数
    def __init__(self, user_name, pass_word,email):
        self.user_name = user_name
        self.email = email
        self.pass_word=pass_word
        #构造函数
    def __init__(self, user_name):
        self.user_name = user_name
      # 密码加密
    def hash_password(self, password):
        self.pass_word = apps.custom_app_context.encrypt(password)
    
    # 密码解析
    def verify_password(self, password):
        return apps.custom_app_context.verify(password, self.pass_word)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    #print 方法打印的内容？
    def __repr__(self):
        return '<User %r>' % self.user_name



db.create_all()
