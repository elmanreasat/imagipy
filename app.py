from flask import Flask, request, render_template, redirect, flash, Response
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img, login, User
import base64
from controllers.upload import upload_images
from controllers.delete import images_to_delete, delete_images
from controllers.display import get_priv_images, get_public_images

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
    return render_template('index.html', user=current_user.email)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
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

        if User.query.filter_by(email=email).first():
            return 'Email already Present'

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
    pic_list_private = get_priv_images(current_user.get_id())
    pic_list_public = get_public_images(current_user.get_id())
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
    if not pic_list:
        return 'No pic uploaded!', 400

    private = request.form.get("privacy") == "true"

    if upload_images(pic_list, private, current_user.get_id()):
        return 'Img Uploaded!', 200
    else:
        return 'Bad upload!', 400


@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    pic_list = images_to_delete(current_user.get_id())
    base64pic_list = {}
    if pic_list is None:
        return redirect('/display')
    for pic in pic_list:
        base64pic = base64.b64encode(pic.img).decode()
        base64pic_list[pic.id] = base64pic

    return render_template('delete.html', image_list=base64pic_list, user=current_user.email)


@app.route('/delete_action', methods=['POST', 'GET'])
@login_required
def delete_action():
    delete_images(current_user.get_id(), request.form.get("user"), request.form.get("delete_all"))
    return redirect('/delete')
