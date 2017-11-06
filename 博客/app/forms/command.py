from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Length,DataRequired

class CommandForm(FlaskForm):
    content=TextAreaField('评论',validators=[DataRequired(),Length(1,128,message='字数超出范围')])
    submit =SubmitField('提交评论 ')