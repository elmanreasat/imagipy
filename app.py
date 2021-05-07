from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///image.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pic_list = request.files.getlist("pics")
    #import pdb; pdb.set_trace()
    if not pic_list:
        return 'No pic uploaded!', 400
    for pic in pic_list:
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype or "image" not in str(mimetype):
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()

    return 'Img Uploaded!', 200