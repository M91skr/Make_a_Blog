"""---------------------------------------- Make a Blog ----------------------------------------
In this code, a blog is designed using Flask.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import requests
from flask import Flask, render_template

# ---------------------------------------- Add Parameters ----------------------------------------

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


if __name__ == "__main__":
    app.run(debug=True)
