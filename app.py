from flask import Flask, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm
csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nothing'}
    posts = [
        {
            'author': {'nickname': 'Alex'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template(
        "index.html",
        title="Main page",
        user=user,
        posts=posts,
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
