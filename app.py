import sqlite3

from flask import Flask, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm
from werkzeug.exceptions import abort

csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object('config')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
@app.route('/index')
def index():

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template(
        "index.html",
        title="Main page",
        posts=posts
    )


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template(
        'post.html',
        post=post
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template(
        'login.html',
        title='Sign In',
        form=form,
        providers=app.config['OPENID_PROVIDERS']
    )


if __name__ == '__main__':
    app.run()
