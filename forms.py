from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    first_name = StringField(label = "First Name", validators = [DataRequired(), Length(min = 3, max = 30)])
    last_name = StringField(label = "Last Name", validators=[DataRequired(), Length(min = 3, max = 30)])
    email = StringField(label = "Email", validators=[DataRequired(), Email(), Length(min = 3, max = 30)]) 
    username = StringField(label = "Username", validators=[DataRequired(), Length(min = 3, max = 30)])
    password1 = PasswordField(label = "Password", validators=[DataRequired(), Length(min = 8, max = 30)])
    password2 = PasswordField(label = "Password", validators=[DataRequired(), Length(min = 8, max = 30)])

class LoginForm(FlaskForm):
    username = StringField(label = "Username", validators=[DataRequired(), Length(min = 3, max = 30)])
    password = PasswordField(label = "Password", validators=[DataRequired(), Length(min = 8, max = 30)])

class ReviewForm(FlaskForm):
    content = TextAreaField(label = "Review", validators = [DataRequired(), Length(min = 3, max = 1000)])

class ContactForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired()])
    email = StringField(label = "Email", validators=[DataRequired(), Email()]) 
    subject = StringField(label = "Subject", validators=[DataRequired()])
    message = TextAreaField(label = "Message", validators = [DataRequired()])

class SubscriberForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired()])
    email = StringField(label = "Email", validators=[DataRequired(), Email()]) 
