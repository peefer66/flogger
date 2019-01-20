from flask_wtf import Flaskform
from wtforms import Stringfield, validators, TextAreaField, SelectField
from wtfforms.ext.sqlalchemy.fields import QuerySelectField

from models_blog import Category

#create categories before it is called in the PostForm
#return a raw category query
def categories():
    return Category.query

class PostForm(Flaskform):
    title = Stringfield('Title', [
        validators.InputRequred(),
        validators.Length(max=80)
    ])
    body = TextAreaField('Content', [
        validators.InputRequred()])

    category = QuerySelectField('Catagory', query_factory=categories,
     allow_blank=True)
    new_category = Stringfield('New Category')