from flask import Blueprint, session, render_template, redirect, flash, url_for
from slugify import slugify

from blog.forms_blog import PostForm
from blog.models_blog import Post, Category
from author.models_author import Author
from application import db
from author.decorators import login_required

blog_app =Blueprint('blog_app', __name__)

@blog_app.route('/')
def index():
    return render_template('blog/index.html')

#we want to make certain routes available if the user is logged in
# eg the post route. So use a decorator  - @login_required
@blog_app.route('/post', methods=('GET', 'POST'))
@login_required # decorator.py
def post():
    form = PostForm()
    # Check for new category
    if form.validate_on_submit():
    # New category 
        if form.new_category.data:
    # Create an instance of the catagory with the description on it
            new_category = Category(form.new_category.data)
    # Add to a new session
            db.session.add(new_category)
    # Generate a category id without saving to DB.
    # flush is like a pre-save allowing a genertion of a new id
    # and keeping the session open for mods without saving to DB
            db.session.flush()
    # assign the new category
            category = new_category
    #If there is no new category assign to whatever is on the drop down
        else:
            category = form.category.data

        # Data base opperations
        author = Author.query.get(session['id']) # This assumes a user is already logged 
        title = form.title.data.strip() # Strip leading and tailing blank
        body = form.body.data.strip()
        # Create a Post sqlalchemy object
        post = Post(author=author, title=title,
         body=body, category=category)
        # save to database
        db.session.add(post)
        db.session.commit()

        # generate a url from slugify
        slug = slugify(str(post.id) + '-' + post.title)
        post.slug = slug
        db.session.commit()

        flash('Article posted')
        return redirect(url_for('.article', slug=slug))
    return render_template('blog/post.html', form=form)


        
@blog_app.route('/post/<slug>')
def article(slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        return render_template('blog/article.html', post=post)

