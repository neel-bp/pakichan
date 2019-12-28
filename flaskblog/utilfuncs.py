import os
import secrets
from PIL import Image
from flaskblog import app
from datetime import timezone

def thread_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    size = 250, 250
    i = Image.open(form_picture)
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg')
    return picture_fn

def post_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    size = 125, 125
    i = Image.open(form_picture)
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg')
    return picture_fn

def utc_to_local(utc_d):
    return utc_d.replace(tzinfo=timezone.utc).astimezone()