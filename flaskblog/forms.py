from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired



class PostForm(FlaskForm):
    name = StringField('Name')
    title = StringField('Title')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    image = FileField('Image',validators=[
        FileRequired(),
        FileAllowed(['jpg','png'])
    ])

class SubPostForm(FlaskForm):
    name = StringField('Name')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    image = FileField('Image',validators=[
        FileAllowed(['jpg','png'])
    ])