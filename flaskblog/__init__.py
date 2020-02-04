from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PERMANENT_SESSION_LIFETIME'] = 60
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
db = SQLAlchemy(app)

# boardlist dictionary
boards = {
    'b':'/b/ - random',
    'cnpol':'/cnpol/ - Culture and Politics',
    'meta':'/meta/ - Meta',
    'tech': '/tech/ - Technology'
}

from flaskblog import routes
