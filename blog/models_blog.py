from datetime import datetime

from application import db

# Association table for Tags Many to Many relationship
tag_x_post = db.Table('tag_x_post',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    #Store the image name and not the binary file on the database
    # 36 chr because going to use a randomly generated hash with UUID
    # that generates strings of 36 characters
    image = db.Column(db.String(36))
    slug = db.Column(db.String(255), unique=True) # Max for varchar indexes
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    author = db.relationship('Author',
                                backref=db.backref('posts', lazy='dynamic'))

    category = db.relationship('Category',
                                backref=db.backref('posts', lazy='dynamic'))

    tags = db.relationship('Tag', secondary=tag_x_post, lazy='subquery',
    backref=db.backref('posts', lazy='dynamic'))

    # This is not a real column on the post table but more of a referance for the 
    # many to many relationship
    def __init__(self, author, title, body, image, category=None,
        slug=None, publish_date=None, live=True):
        self.author_id = author.id
        self.title = title
        self.body = body
        self.image = image
        if category:
            self.category_id = category.id
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

# Association table for many to many relationship
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

