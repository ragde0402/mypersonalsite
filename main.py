import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from forms import CreatePostForm, LoginForm, ContactForm, CreatePortfolio

# Mail configuration
mailertogo_host = os.environ.get('MAILERTOGO_SMTP_HOST')
mailertogo_port = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
mailertogo_user = os.environ.get('MAILERTOGO_SMTP_USER')
mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
mailertogo_domain = os.environ.get('MAILERTOGO_DOMAIN', "edgarmolecki.xyz")

sender_user = 'noreply'
sender_email = "@".join([sender_user, mailertogo_domain])
sender_name = 'My site'

recipient_email = os.environ.get("TO_MAIL")
recipient_name = "Edgar's site"

subject = 'Mail from personal site'

# app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/preprogramming")
def preprogramming():
    return render_template("preprogramming.html", current_user=current_user)


@app.route("/programming")
def programming():
    portfolio = Portfolio.query.all()
    return render_template("programming.html", current_user=current_user, list=portfolio)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            message = form.body.data

            body_plain = f"name: {name}\nemail: {email}\nphone: {phone}\nmessage: {message}"
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = utils.formataddr((sender_name, sender_email))
            message['To'] = utils.formataddr((recipient_name, recipient_email))
            part1 = MIMEText(body_plain, 'plain')
            message.attach(part1)

            server = smtplib.SMTP(mailertogo_host, mailertogo_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mailertogo_user, mailertogo_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            server.close()

            flash("Your message was sent successfully.")
            return redirect(url_for("contact"))
        flash("Oops something went wrong. Check all the fields and fill them correctly.")
        return render_template("contact.html", current_user=current_user, form=form)
    return render_template("contact.html", current_user=current_user, form=form)


@app.route("/blog")
def blog():
    return render_template("blog.html", current_user=current_user)


@app.route("/post/<int:num>")
def post(num):
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = Users.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("blog", logged_in=current_user.is_authenticated))
    return render_template("login.html", form=form, current_user=current_user)


@app.route("/new_post")
@login_required
def new_post():
    form = CreatePostForm()
    return render_template("new_post.html", current_user=current_user, form=form)


@app.route("/new_portfolio", methods=["POST", "GET"])
@login_required
def new_portfolio():
    form = CreatePortfolio()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.project_name.data
            subtitle = form.subtitle.data
            img_url = form.img_url.data
            project_url = form.project_url.data
            description = form.description.data.replace("<p>", "").replace("</p>", "")
            new_portfolio_project = Portfolio(
                project_name=name,
                subtitle=subtitle,
                img_url=img_url,
                url=project_url,
                description=description,
            )
            db.session.add(new_portfolio_project)
            db.session.commit()
        else:
            redirect(url_for("home"))
            return
        return redirect(url_for("programming"))
    return render_template("new_post.html", current_user=current_user, form=form)


@app.route("/delete/<int:num>")
@login_required
def delete():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home", current_user=current_user))


if __name__ == "__main__":
    app.run(debug=True)
