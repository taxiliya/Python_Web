import os
import time,platform
from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask import Flask, render_template,request,send_from_directory

import config
from forms import BaseLogin,UploadForm

app = Flask(__name__,static_folder='static')
# static_folder 自定义静态文件夹
app.config.from_object(config.DbConfig)
db=SQLAlchemy(app)

class Book (db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    publish_office=db.Column(db.String(100),nullable=False)
    ISSN=db.Column(db.String(100),nullabLe=False)
    storage_time=db.Column(db.DateTime,default=DateTime.now)

db.create_all()

if platform.system()=='Windows':
    slash='\\'
else:
    slash='/'
UPLOAD_PATH=os.path.curdir+slash+'uploads'+slash

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = BaseLogin()
    if form.validate_on_submit():
        return '表单数据提交成功!'
    else:
        return render_template('login.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method=='GET':
        return render_template('upload.html')
    else:
        if not os.path.exists(UPLOAD_PATH):
            os.mkdir(UPLOAD_PATH)
        form=UploadForm(CombinedMultiDict([request.form,request.files]))
        if form.validate():
            f=request.files['file']
            filename=secure_filename(f.filename)
            ext=os.path.splitext(filename)[1]
            os_time=int(time.time())
            new_filename=str(os_time)+ext
            f.save(os.path.join(UPLOAD_PATH,new_filename))
            return '上传成功'
        else:
            return '上传错误，仅支持jpg,png,gif'

@app.route('/image/<filename>', methods=['GET', 'POST'])
def get_image(filename):
    dir_path=os.path.join(app.root_path,'uploads')
    return send_from_directory(dir_path,filename)

@app.errorhandler(404)
    # 不存在页
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
    # 错误页
def internal_server_error(e):
    return render_template('500.html')

@app.route('/cat')
    # 静态文件加载：image、css
def cat():
    return render_template('cat.html')

@app.route('/zifucanshu/<username>')
def user(username):
    return '<h1>hello %s </h1>' % username

@app.route('/shuzhicanshu/<int:id>')
def user_list(id):
    user_list=['用户1','用户2','用户3']
    if id < len(user_list):
        return '<h1>hello %s </h1>' % user_list[id]
    else:
        return 'Error number'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # return 'User %s' % username
    # username=username
    # return render_template('user.html', username=username)
    return render_template('user.html', **locals())

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)