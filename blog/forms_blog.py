from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from blog.models_blog import Category

#create categories before it is called in the PostForm
#return a raw category query
def categories():
    return Category.query

class PostForm(FlaskForm):
    title = StringField('Title', [
        validators.InputRequired(),
        validators.Length(max=80)
    ])
    body = TextAreaField('Content', [
        validators.InputRequired()])

    category = QuerySelectField('Catagory', query_factory=categories,
     allow_blank=True)
    new_category = StringField('New Category')