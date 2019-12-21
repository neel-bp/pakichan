from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    name = StringField('Name')
    title = StringField('Title')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SubPostForm(FlaskForm):
    name = StringField('Name')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')