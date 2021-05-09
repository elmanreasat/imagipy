from db import db
from models import Img


def images_to_delete(user_id):
    pic_list = Img.query.filter_by(user_id=user_id)
    return pic_list

def delete_images(user_id, image_id, delete_all):
    if delete_all:
        Img.query.filter_by(user_id=user_id).delete()
    else:
        Img.query.filter_by(id=image_id).delete()
    db.session.commit()
    return True