from flask import Blueprint, session, render_template

from blog.forms_blog import PostForm
from blog.models_blog import Post, Category
from author.models_author import Author

blog_app =Blueprint('blog_app', __name__)

@blog_app.route('/')
def index():
    return render_template('blog/index.html')

@blog_app.route('/post', methods=('GET', 'POST'))
def post():
    form = PostForm()
    return render_template('blog/post.html', form=form)