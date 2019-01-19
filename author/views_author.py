from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash

from author.models_author import Author
from author.forms_author import RegisterForm
from application import db

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # If the user input is valid
    if form.validate_on_submit():
        # Python debugger
        import pdb; pdb.set_trace()
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

        return f'Author ID: {author.id}'
        
    return render_template('author/register.html', form=form)