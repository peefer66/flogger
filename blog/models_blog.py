from datetime import datetime
from models_author import Author


from application import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    catagory_id= db.Column(db.Integer,db.ForeignKey('catagory.id'))
    author_id= db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    slug = db.Column(db.String(255), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    author = db.relationship('Author', db.backref('posts', lazy='dynamic'))
    catagory = db.relationship('Catagory',db.backref('posts', lazy='dynamic'))

    def __init__(self, author, title, body, catagory=None,
        slug=None, publish_date=None, live=True):

        self.author_id = author.id
        self.title = title
        self.body = body
        if catagory:
            self.catagory_id = catagory.id
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()()
        self.live = live

    def __repr__(self):
        return '<Post %r>' %self.title

class Category(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name

