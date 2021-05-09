from flask import Flask, request, render_template, redirect, flash, Response
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img, login, User
import base64


app = Flask(__name__)
app.secret_key = 'xyz'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///image.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init(app)
login.init_app(app)
login.login_view = 'login'


@app.route('/')
def first():
    return redirect('/home')


@app.route('/home')
@login_required
def blog():
    #import pdb; pdb.set_trace()
    return render_template('index.html', user=current_user.email)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        #import pdb;pdb.set_trace()
        return redirect('/home')

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        #import pdb; pdb.set_trace()
        if user is not None and user.check_password(request.form['password']):
            #import pdb;pdb.set_trace()
            login_user(user)
            return redirect('/home')
        else:
            flash('No user found')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #import pdb;pdb.set_trace()

        if User.query.filter_by(email=email).first():
            return ('Email already Present')

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

    
@app.route('/display')
def display():
    pic_list_private = Img.query.filter_by(user_id=current_user.get_id())
    pic_list_public = db.session.query(Img).filter(
        and_(
            Img.user_id != current_user.get_id(),
            Img.private == False
        )
    )
    base64pic_list = []
    for pic in pic_list_private:
        base64pic = base64.b64encode(pic.img).decode()
        base64pic_list.append(base64pic)

    for pic in pic_list_public:
        base64pic = base64.b64encode(pic.img).decode()
        base64pic_list.append(base64pic)


    return render_template('display.html', image_list = base64pic_list, user=current_user.email)


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    pic_list = request.files.getlist("pics")
    #import pdb;pdb.set_trace()
    if not pic_list:
        return 'No pic uploaded!', 400
    for pic in pic_list:
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        user_id = current_user.get_id()
        private = False
        if request.form.get("privacy") == "true":
            private = True
        if not filename or not mimetype or "image" not in str(mimetype):
            return 'Bad upload!', 400

        img = Img(img=pic.read(), user_id=user_id, private=private,name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    pic_list = Img.query.filter_by(user_id=current_user.get_id())
    base64pic_list = {}
    #import pdb;pdb.set_trace()
    if pic_list is None:
        return redirect('/display')
    for pic in pic_list:
        base64pic = base64.b64encode(pic.img).decode()
        base64pic_list[pic.id] = base64pic

    return render_template('delete.html', image_list=base64pic_list, user=current_user.email)


@app.route('/delete_action', methods=['POST', 'GET'])
@login_required
def delete_action():
    #import pdb;pdb.set_trace()
    if request.form.get("delete_all"):
        Img.query.delete()
    else:
        Img.query.filter_by(id=request.form.get("user")).delete()
    db.session.commit()
    return redirect('/delete')
