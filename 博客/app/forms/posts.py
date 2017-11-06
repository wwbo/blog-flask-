from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Length,DataRequired

class PostsForm(FlaskForm):
    content=TextAreaField('这一刻的心情',validators=[DataRequired(),Length(1,128,message='字数超出范围')])
    submit =SubmitField('发表 ')

