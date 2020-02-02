# server side code

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, join_room, send
from config import Config
from login import LoginForm, RegisterForm

# initialize Flask
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins='*')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

# home page
@app.route('/')
def index():
    return render_template('index.html')



def message_received():
    print("message was received")


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
    socketio.run(app, debug=True)

"""

# listen for events
@socketio.on('create game')
def on_create(data):
    emit('new game: ' + str(room))
    # ROOMS.append(room + 1)
    ROOMS.append(data)
    print(ROOMS)
"""