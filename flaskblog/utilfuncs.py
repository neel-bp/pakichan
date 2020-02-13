import os
import secrets
from PIL import Image
from flaskblog import app
from datetime import timezone
from bleach import clean, linkify
from markupsafe import Markup
import re
import html
from flaskblog.models import get_class_by_tablename
from sqlalchemy import and_

def thread_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    i = Image.open(form_picture)
    width, height = i.size
    if width <= 250:
        size = width,width
    else:
        size = 250,250
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg',quality=95)
    return picture_fn

def post_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    i = Image.open(form_picture)
    width,height = i.size
    if width <= 125:
        size = width,width
    else:
        size = 125,125
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg',quality=95)
    return picture_fn

def utc_to_local(utc_d):
    return utc_d.replace(tzinfo=timezone.utc).astimezone()

# functions for white listing html tags in jinja templates
def do_clean(text, **kw):
    """Perform clean and return a Markup object to mark the string as safe.
    This prevents Jinja from re-escaping the result."""
    return Markup(clean(text, **kw))

# regex and replace for greentexting
def greentext(m):
    return f'<span class="greentext">{m.group(0)}</span>'

def greenregex(content):
    return re.sub(r'^>.*',greentext,content,flags=re.MULTILINE)

# regex and replace for href jumping
def href(m):
    return f'<a href=#{m.group(0)[2:]}>{m.group(0)}</a>'

def hrefregex(content):
    return re.sub(r'>>[0-9]*',href,content)

# jijnja filter for moment.js for converting datetime to client timezone
def moment(date):
    return Markup(f'<script>document.write(moment("{str(date)}"+"Z").format("DD/MM/YY(ddd)HH:mm:ss"))</script>')

def linky(content):
    linkified_text = linkify(content)  # it linkifies text but unescape everything else
    return html.unescape(linkified_text)  # unescaping linkified text

# regex and replace for spoiler text
def spoiler(m):
    return f'<span class="spoiler">{m.group(1)}</span>'

def spoilerregex(content):
    return re.sub(r'\[s\](.*?)\[\/s\]',spoiler,content)

# combining all regex
def allRegex(content):
    return spoilerregex(greenregex(linky(content)))




# content circulation, whenever threads exceed 7 (for now) it will delete the least active thread, or bottom most thread
def bumpOrderThreshold(boardname):
    threads=[]
    for i in get_class_by_tablename(boardname).query.order_by(get_class_by_tablename(boardname).date_posted.desc()).all():
        if i.parent is None and i not in threads:
            threads.append(i)
        elif i.parent is not None and i.parent not in threads:
            threads.append(i.parent)
    if len(threads) > 200:
        return threads[len(threads) - 1]
    else:
        return 'maxLimitNotReached'

def post_replies(boardname, thread_id, post_id):
    li=[]
    posts = get_class_by_tablename(boardname).query.filter(and_(get_class_by_tablename(boardname).parent_id == thread_id, get_class_by_tablename(boardname).content.ilike(f'%<a href=#{post_id}>>>{post_id}</a>%'))).all()
    for i in posts:
        li.append(i.id)
    return li