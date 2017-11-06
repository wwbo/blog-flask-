from app.extensions import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(30),unique=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(64),default='default.jpg')

    posts = db.relationship('Posts',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码是不可读属性')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_passwd(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            return False
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
        return True

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))