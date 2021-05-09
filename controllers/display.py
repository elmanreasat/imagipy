from sqlalchemy import and_

from db import db
from models import Img


def get_priv_images(user_id):
    pic_list_private = Img.query.filter_by(user_id=user_id)
    return pic_list_private


def get_public_images(user_id):
    pic_list_public = db.session.query(Img).filter(
        and_(
            Img.user_id != user_id,
            Img.private == False
        )
    )
    return pic_list_public
