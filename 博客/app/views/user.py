from flask import Blueprint,render_template,flash,redirect,url_for,current_app,request
from app.forms import RegisterForm,LoginForm,PasswordForm,EmailForm,FindForm,IconForm
from app.email import send_mail
from app.models import User
from app.extensions import db,photos
from flask_login import login_user,logout_user,login_required,current_user
import os
from PIL import Image
user = Blueprint('user',__name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建对象
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 写入数据库
        db.session.add(u)
        # 因为下面产生token时需要用到用户id，此时还没有用户id
        db.session.commit()
        # 生成token
        token = u.generate_activate_token()
        # 发送激活邮件
        send_mail(form.email.data, '账户激活', 'email/account_activate', token=token, username=form.username.data)
        flash('激活邮件已发送，请点击链接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账号激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('账号激活失败')
        return redirect(url_for('main.index'))

@user.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('用户名不存在')
        elif u.verify_passwd(form.password.data):
            login_user(u,remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('user/login.html',form=form)

@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')

@user.route('/change_password/',methods=['GET','POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.verify_passwd(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            db.session.add(current_user)
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('原始密码出错')
            return redirect(url_for('user.change_password.html'))

    return render_template('user/change_password.html',form=form)

@user.route('/change_email/',methods=['GET','POST'])
@login_required
def change_email():
    form = EmailForm()
    if form.validate_on_submit():
        if current_user.email == form.old_email.data:
            current_user.confirmed = False
            db.session.add(current_user)
            db.session.commit()
            token = current_user.generate_activate_token()

            send_mail(current_user.email, '账号重置', 'email/account_activate', token=token, username=current_user.username)
            current_user.email = form.new_email.data
            # current_user.confirmed = True
            # db.session.add(current_user)
            flash('邮箱发送成功')
            return redirect(url_for('main.index'))
        else:
            flash('原始邮箱不存在')
            return redirect(url_for('user.change_email.html'))
    return render_template('user/change_email.html',form=form)

@user.route('/email_find/<token>')
def email_find(token):
    if User.check_activate_token(token):
        # current_user.email = form.new_email.data
        current_user.confirmed = True
        db.session.add(current_user)
        flash('邮箱更改成功')
        return redirect(url_for('user.login'))
    else:
        flash('邮箱更改失败')
        return redirect(url_for('main.index'))


@user.route('/find_password/',methods=['GET','POST'])
def find_password():
    form = FindForm()
    # if form.validate_on_submit():
    #     if User.query.filter_by(email=form.find_email.data):
    #         return render_template('')
    #
    #     else:
    #         flash('邮箱错误')

    return render_template('user/find_password.html',form=form)

@user.route('/change_icon/',methods=['GET','POST'])
@login_required
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.icon.data.filename)[1]
        name = rand_str() + suffix
        photos.save(form.icon.data,name=name)
        pathname = os.path.join(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],name))
        img = Image.open(pathname)
        img.thumbnail((64,64))
        img.save(pathname)
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        current_user.icon = name
        db.session.add(current_user)
        flash('头像已更改')
    return render_template('user/change_icon.html',form=form)

def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in
                   range(length))