from flask import request
from werkzeug.utils import secure_filename

from db import db
from models import Img


def upload_images(pic_list, private, user_id):
    #import pdb; pdb.set_trace()
    for pic in pic_list:
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        if not filename or not mimetype or "image" not in str(mimetype):
            return False

        img = Img(img=pic.read(), user_id=user_id, private=private, name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
    return True
