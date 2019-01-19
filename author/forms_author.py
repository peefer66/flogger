from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from werkzeug.security import check_password_hash

from author.models_author import Author

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired()])
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password',[
        validators.InputRequired(),
        validators.Length(min=4, max=80)
    ])
    confirm = PasswordField('Repeat Password', [validators.EqualTo('password',message='Passwords must match')
    ])

    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = EmailField('Email Adress', [validators.InputRequired(),validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=4, max=80)])

    # validate the user and passowrd with the database
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        # Create instance of Author and query on email
        author = Author.query.filter_by(email=self.email.data).first()
        # If email exists in database 
        if author:
            # If password incorrect 
            if not check_password_hash(author.password, self.password.data):# Compare password with hashed password
                self.password.errors.append('Incorrect email or password') # always error both the email and password!!
                return False
            return True
        # email doesn't existin database
        else:
            return 'Incorrect email or password'
