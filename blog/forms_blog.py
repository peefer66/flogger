from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileAllowed

from blog.models_blog import Category

#create categories before it is called in the PostForm
#return a raw category query
def categories():
    return Category.query

class PostForm(FlaskForm):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'We only accept JPG or PNG files')
    ])
    title = StringField('Title', [
        validators.InputRequired(),
        validators.Length(max=80)
    ])
    body = TextAreaField('Content', [
        validators.InputRequired()])

    category = QuerySelectField('Catagory', query_factory=categories,
     allow_blank=True)
    new_category = StringField('New Category')