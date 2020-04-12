from datetime import datetime
from flaskblog import db


class Random(db.Model):
    __tablename__ = 'b'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default="Anonymous")
    title = db.Column(db.String(100), nullable=True)
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('b.id'))
    image_file = db.Column(db.String(20), nullable=True)
    parent = db.relationship('Random', primaryjoin=('Random.parent_id==Random.id'),remote_side=id, backref='subpost')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}, {self.id}, {self.parent_id}')"

class Technology(db.Model):
    __tablename__ = 'tech'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default="Anonymous")
    title = db.Column(db.String(100), nullable=True)
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    image_file = db.Column(db.String(20), nullable=True)
    parent = db.relationship('Technology', primaryjoin=('Technology.parent_id==Technology.id'),remote_side=id, backref='subpost')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}, {self.id}, {self.parent_id}')"

class CultureAndPolitics(db.Model):
    __tablename__ = 'cnpol'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default="Anonymous")
    title = db.Column(db.String(100), nullable=True)
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('cnpol.id'))
    image_file = db.Column(db.String(20), nullable=True)
    parent = db.relationship('CultureAndPolitics', primaryjoin=('CultureAndPolitics.parent_id==CultureAndPolitics.id'),remote_side=id, backref='subpost')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}, {self.id}, {self.parent_id}')"

class Meta(db.Model):
    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default="Anonymous")
    title = db.Column(db.String(100), nullable=True)
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('meta.id'))
    image_file = db.Column(db.String(20), nullable=True)
    parent = db.relationship('Meta', primaryjoin=('Meta.parent_id==Meta.id'),remote_side=id, backref='subpost')


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}, {self.id}, {self.parent_id}')"

class CoolDown(db.Model):
    __tablename__ = 'cooldown'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"CoolDown('{self.id}', '{self.ip}, {self.date_posted}')"

# get model by tablename
def get_class_by_tablename(tablename):
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c