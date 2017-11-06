import os
from flask_bootstrap import Bootstrap
base_dir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwertyuiopasdfghjklzxcvbnm1234567890'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '17670426005@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'wangwenbo199610'
    BOOTSTRAP_SERVER_LOCAL=True
    MAX_CONTENT_LENGTH = 12 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'blog-dev.sqlite')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'splite:///' + os.path.join(base_dir,'blog-test.sqlite')

class ProductionConfig(Config):
    SQLALCHMEY_DATABASE_URI = 'splite:///'+ os.path.join(base_dir,'blog.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig,
}