from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,ValidationError,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from app.models import User
from  flask_wtf.file import FileField,FileAllowed,FileRequired
from app.extensions import photos

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,18,message='6-18个字符')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,18,message='密码长度6-18')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message='密码不一致')])
    email = StringField('邮箱',validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('注册')

    def validata_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已存在')

    def validata_email(self,filed):
        if User.query.filter_by(email= filed.data).first():
            raise ValidationError('该邮箱已被注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField("记住密码")
    submit = SubmitField('立即登录')

class PasswordForm(FlaskForm):
    old_pwd = PasswordField('原密码',validators=[DataRequired()])
    new_pwd = PasswordField('新密码',validators=[DataRequired(),Length(6,18,message='长度6-18')])
    confirm = PasswordField('确认密码',validators=[EqualTo('new_pwd',message='密码不一致')])
    submit = SubmitField('立即修改')

class EmailForm(FlaskForm):
    old_email = StringField('原邮箱',validators=[Email('邮箱格式错误')])
    new_email = StringField('新邮箱',validators=[Email('邮箱格式错误')])
    confirm = StringField('确认邮箱',validators=[EqualTo('new_email',message='邮箱不一致')])
    submit = SubmitField('确认修改')

class FindForm(FlaskForm):
    find_email = StringField('注册的邮箱号',validators=[Email('邮箱格式错误')])
    submit = SubmitField('找回')

class IconForm(FlaskForm):
    icon = FileField('头像',validators=[FileRequired('请选择上传头像'),FileAllowed(photos,'只能上传图片')])
    submit = SubmitField('上传')