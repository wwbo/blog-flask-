from flask import Blueprint,render_template,current_app,flash,redirect,url_for,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.forms import PostsForm,CommandForm
from app.models import Posts,User
from flask_login import current_user
from app.extensions import db
main = Blueprint('main',__name__)


@main.route('/',methods=['GET','POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u =current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表')
            return redirect('user.login')
    # posts = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    page = request.args.get('page',1,type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=3,error_out=False)
    posts = pagination.items
    return render_template('main/index.html',form=form,posts=posts,pagination=pagination)





@main.route('/detail/<name>',methods = ['get','post'])
def detail(name):

    uid = User.query.filter_by(username=name).first().id

    # posts = Posts.query.filter_by(uid=id).all()
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(uid=uid,rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=False)
    posts = pagination.items
    return render_template('main/detail.html',name=name,posts = posts,pagination=pagination )


@main.route('/command/<port>',methods=['GET','POST'])
def command(port):
    form = CommandForm()
    id = Posts.query.filter_by(content=port).first().id
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u =current_user._get_current_object()
            p = Posts(content=form.content.data,user=u,rid=id)
            db.session.add(p)
            return redirect(url_for('main.command',port=port))
        else:
            flash('登录后才能评论')
            return redirect('user.login')

    page = request.args.get('page',1,type=int)
    pagination = Posts.query.filter_by(rid=id).order_by(Posts.timestamp.desc()).paginate(page,per_page=3,error_out=False)
    posts = pagination.items
    return render_template('main/command.html',form=form,posts=posts,pagination=pagination,port=port)


