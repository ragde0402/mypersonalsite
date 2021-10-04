from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreatePortfolio(FlaskForm):
    project_name = StringField("Project name", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    project_url = StringField("Project URL", validators=[DataRequired(), URL()])
    description = CKEditorField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit Portfolio")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Enter the correct email.")])
    phone = StringField("Phone", validators=[DataRequired()])
    body = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")
