"""---------------------------------------- Make a Blog ----------------------------------------
In this code, a blog is designed using Flask.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import requests
from flask import Flask, render_template, request
import smtplib

# ---------------------------------------- Add Parameters ----------------------------------------

email_from = "MY_EMAIL"
email_pass = "MY_PASSWORD"

# ---------------------------------------- Site-Rendering ----------------------------------------

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog')
def get_blog():
    blog_url = "https://api.npoint.io/27ecb044dcad72bd9766"
    response_blog = requests.get(blog_url)
    all_post = response_blog.json()
    return render_template('blog.html', posts=all_post)


@app.route('/blog/<int:num>')
def post(num):
    blog_url = "https://api.npoint.io/27ecb044dcad72bd9766"
    response_blog = requests.get(blog_url)
    all_post = response_blog.json()
    return render_template('post.html', post=all_post, post_id=num)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/login", methods=["POST"])
def login():
    name = request.form["cl_name"]
    email = request.form["cl_email"]
    question = request.form["cl_ques"]
    print(name)
    print(email)
    print(question)
    message = "Ihre Nachricht wurde erfolgreich gesendet,Ich antworte dir innerhalb der nächsten 3 Tage."
    send_email(name, email, message)
    return "<h1>Ihre Nachricht wurde erfolgreich gesendet.</h1>"


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(email_from, email_pass)
        connection.sendmail(email_from, email, email_message)


if __name__ == "__main__":
    app.run(debug=True)
