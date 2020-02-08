from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired



class PostForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100)])
    title = StringField('Title', validators=[Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post')
    image = FileField('Image',validators=[
        FileRequired(),
        FileAllowed(['jpg','png'])
    ])

class SubPostForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post')
    image = FileField('Image',validators=[
        FileAllowed(['jpg','png'])
    ])