from flask import Blueprint, session, render_template

blog_app =Blueprint('blog_app', __name__)

@blog_app.route('/')
def index():
    return render_template('blog/index.html')