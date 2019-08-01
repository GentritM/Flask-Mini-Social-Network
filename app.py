from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, GoogleForm
from flask_dance.contrib.google import make_google_blueprint, google
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = '255890dd847ced350c035706b929657b'

blueprint = make_google_blueprint(
    client_id='',
    client_secret='',
    offline=True,
    scope=['profile', 'email']
)
app.register_blueprint(blueprint,url_prefix='/login')

posts = [
    {
        'author':'lavdim',
        'title':'post 1',
        'content':'firstasda',
        'date':'april 12'
    },
    {
        'title': 'post 2',
        'author':'brajan',
        'content':'my post',
        'date':'april 13'
    }
]
@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    title = 'About'
    return render_template('about.html', title=title)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('{} has been registered successfully'.format(form.username.data), 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()


    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)



@app.route('/login/google')
def login_google():

    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('login.html', email=email)

if __name__ == '__main__':
    app.run()
