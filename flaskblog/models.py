from datetime import datetime
from flaskblog import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default='Anonymous')
    title = db.Column(db.String(100), nullable=True, default='Thread')
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent = db.relationship('Post', primaryjoin=('Post.parent_id==Post.id'),remote_side=id, backref='subpost')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}, {self.id}, {self.parent_id}')"