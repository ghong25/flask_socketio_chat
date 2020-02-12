from flask import redirect, url_for, render_template, flash
from login import LoginForm, RegisterForm

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, login_required, current_user, login_user

import models


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)


# login page
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    # if user is authenticated then redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('/user_login'))
        login_user(user)
        return redirect('/index')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return '<h1> New user has been created </h1>'

    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# home page
@app.route('/')
@app.route('/index')
@login_required
def index():
    print("index")
    return render_template('index.html')


def message_received():
    print("message received")


@socketio.on('my message')
def handle_custom_event(json):
    print('received message: ' + str(json))
    socketio.emit('my response', json, callback=message_received)


# show that client has connected
@socketio.on('connect')
def client_connect():
    print('connected')


@socketio.on('disconnect')
def client_disconnect():
    print('disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
