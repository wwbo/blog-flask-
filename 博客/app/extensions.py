from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)

def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'

    login_manager.login_view = 'user.login'
    login_manager.login_message = '需要登录才能访问'

    configure_uploads(app,photos)
    patch_request_class(app,size=None)



