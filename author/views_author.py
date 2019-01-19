from flask import Blueprint, render_template, url_for, session, redirect
from werkzeug.security import generate_password_hash

from author.models_author import Author
from author.forms_author import RegisterForm, LoginForm
from application import db

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # If the user input is valid
    if form.validate_on_submit():
        # Python debugger
        #import pdb; pdb.set_trace()
        # Generate an hashed password
        hashed_password = generate_password_hash(form.password.data)
        #Create an instance of the Authot
        author = Author(
            form.full_name.data,
            form.email.data,
            hashed_password
        )
        #Save to database
        db.session.add(author)
        db.session.commit()
        # Print to web
        return f'Author ID: {author.id}'
    # If not validate re-load register page 
    return render_template('author/register.html', form=form)

@author_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        #Create 2 sessions for the Author id and full name
        author = Author.query.filter_by(email=form.email.data).first()
        session['full_name'] = author.full_name
        session['id']= author.id 
        return redirect(url_for('blog_app.index'))
    # If he login is invalid refresh the login page
    return render_template('author/login.html', form=form, error=error)

