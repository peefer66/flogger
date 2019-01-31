import os
import uuid
from flask import Blueprint, session, render_template, redirect, flash, url_for, request
from slugify import slugify
from PIL import Image

from blog.forms_blog import PostForm
from blog.models_blog import Post, Category
from author.models_author import Author
from application import db
from author.decorators import login_required
from settings import BLOG_POST_IMAGES_PATH


blog_app =Blueprint('blog_app', __name__)
POSTS_PER_PAGE = 5

@blog_app.route('/')
@login_required
def index():
    # Pagination
    # Define a page variable that will define a page parameter being passed to the route
    # if none it will assigne the number 1 to it
    # Daisy chain paginate has three parameters page we are on, how many post on the page we want and if we want to
    # force a 404 error if forced to another page
    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', posts=posts)


#we want to make certain routes available if the user is logged in
# eg the post route. So use a decorator  - @login_required
@blog_app.route('/post', methods=('GET', 'POST'))
@login_required # decorator.py
def post():
    form = PostForm()

    # Check for new category
    if form.validate_on_submit():

        image_id = None
            #Check for image
            #Generate a random id of 36 chrs
            # convert all to png
            # create a file path
            # save to file path
        if form.image.data:
            f = form.image.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            file_path = os.path.join(
                BLOG_POST_IMAGES_PATH, file_name
                    )
            Image.open(f).save(file_path)
            # save large version for article template and small for index template
            _image_resize(BLOG_POST_IMAGES_PATH, image_id,600, 'lg')
            _image_resize(BLOG_POST_IMAGES_PATH, image_id, 300,'sm')
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
        post = Post(author=author,
             title=title,
             body=body,
             image=image_id,
             category=category
             )
        # save to database
        db.session.add(post)
        db.session.commit()

        # generate a url from slugify
        slug = slugify(str(post.id) + '-' + post.title)
        post.slug = slug
        db.session.commit()

        flash('Article posted')
        return redirect(url_for('.article', slug=slug))
        # if its a new post, submit action=new to the template
    return render_template('blog/post.html', form=form, action='new')

@blog_app.route('/edit/<slug>', methods=('GET', 'POST'))
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = post.image
        original_title = post.title
        form.populate_obj(post)

        if form.image.data:
            f = form.image.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            file_path = os.path.join(
                BLOG_POST_IMAGES_PATH, file_name
            )
            Image.open(f).save(file_path)

            _image_resize(BLOG_POST_IMAGES_PATH, image_id, 600, 'lg')
            _image_resize(BLOG_POST_IMAGES_PATH, image_id, 300, 'sm')

            post.image = image_id
        else:
            post.image = original_image

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category

        if form.title.data != original_title:
            post.slug = slugify(str(post.id) + '-' + form.title.data)

        db.session.commit()
        flash('Article edited')
        return redirect(url_for('.article', slug=post.slug))

    return render_template('blog/post.html',
        form=form,
        post=post,
        action="edit"
    )


# Delete an article
@blog_app.route('/delete/<slug>', methods=('GET','POST'))
@login_required
def delete(slug):
    #Creat instance
    post = Post.query.filter_by(slug=slug).first_or_404()
    # Flag live to false - not actually deleting the article but hiding it
    post.live = False
    # update database
    db.session.commit()
    flash('Article deleted')
    return redirect(url_for('.index'))



@blog_app.route('/post/<slug>')
def article(slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        return render_template('blog/article.html', post=post)


def _image_resize(original_file_path,image_id, image_base, extension):
    # This function resizes the image width keeping the height
    # proportioanl so not to deform the aspect ratio
    file_path = os.path.join(
        original_file_path, image_id + '.png'
    )
    image = Image.open(file_path)
    wpercent = (image_base / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((image_base, hsize), Image.ANTIALIAS)
    modified_file_path = os.path.join(
        original_file_path, image_id + '.' + extension + '.png'
    )
    image.save(modified_file_path)
    return
