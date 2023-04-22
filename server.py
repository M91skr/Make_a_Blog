"""---------------------------------------- Make a Blog ----------------------------------------
In this code, a blog about Iran is designed using Flask.
We can create new blog posts, edit posts and delete posts.
Also, the user can send his question through the contact form and
receive an email containing the answer within a few days.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import os
import smtplib
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

# ---------------------------------------- Add Parameters ----------------------------------------

email_from = "MY_EMAIL"
email_pass = "MY_PASSWORD"

# ---------------------------------------- App Creation ----------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# ---------------------------------------- DB Connection ----------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# ---------------------------------------- WTF Form Creation ----------------------------------------


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

# ---------------------------------------- Site-Rendering ----------------------------------------


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog')
def get_blog():
    posts = BlogPost.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/blog/<int:num>')
def post(num):
    requested_post = BlogPost.query.get(num)
    return render_template('post.html', post=requested_post)


@app.route('/new-post', methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["POST"])
def message():
    name = request.form["cl_name"]
    email = request.form["cl_email"]
    question = request.form["cl_ques"]
    print(name)
    print(email)
    print(question)
    message = "Ihre Nachricht wurde erfolgreich gesendet, Ich antworte dir innerhalb der naechsten drei Tage."
    send_email(name, email, message)
    return "<h1>Ihre Nachricht wurde erfolgreich gesendet.</h1>"


def send_email(name, email, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(os.getenv(email_from), os.getenv(email_pass))
        connection.sendmail(os.getenv(email_from), email, email_message)


if __name__ == "__main__":
    app.run(debug=True)
