a 4chan like imageboard built in python flask,
its still a work in progress, still have a bit i want to add to it,

currently it uses sqlite, but you can easily change to postgres or something easily,
checkout __init__.py and replace 'SQLALCHEMY_DATABASE_URI' to your database url.

also to create or edit boards, just do so in models.py and edit boards dictionary in __init__.py


for test run do the following

git clone https://github.com/neelu0/pakichan.git
cd pakichan
mkdir venv
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt

after above is all done and good
start python in current directory and do this:

from flaskblog import db
db.drop_all()
db.create_all()

thats it you're done.
now start the server by
running run.py
