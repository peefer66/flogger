from flask_wtf import FlaskForm
from wtforms import Validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    full_name = StringFiield('Full Name', [validators.InputRequired()])
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password',[
        validators.InputRequired(),
        validators.Length(min=4, max=80)
    ])
    confirm = PasswordField('Repeat Password', [validators.Equalto(message='Passwords must match')
    ])