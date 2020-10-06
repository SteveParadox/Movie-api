import os
import secrets

from PIL import Image
from flask import current_app


def save_img(form_photo):
    if form_photo:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_photo.filename)
        path = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/movies', path)
        size = (625, 625)
        form_photo.save(picture_path)

        return path
