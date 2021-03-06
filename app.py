from flask import redirect, url_for, render_template, flash, json, jsonify
from login import LoginForm, RegisterForm

from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, join_room, leave_room
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, login_required, current_user, login_user
from pytz import timezone

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)

from models import *


# login page
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    # if user is authenticated then redirect to homepage
    if current_user.is_authenticated:
        print(str(current_user)[6:] + " is authenticated")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user_login'))
        login_user(user)
        return redirect('/index')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect('/index')

    return render_template('signup.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def create_room(user1, user2):
    # return string for new room that has users sorted alphabetically
    return "_".join(sorted([user1, user2], key=str.lower))


# home page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    users = [str(n) for n in User.query.all() if n != current_user]
    current = str(current_user)[6:]

    if request.method == 'POST':
        # second user that you're trying to chat with
        user2 = request.form['test']

        room_id = create_room(current, user2)
        print(room_id)

        # with button click, send user to the new private room
        return redirect('/chat_room/' + room_id)

    return render_template('home.html', users=users, username=current)


# when you click on a username, routes you to a room with that user
@app.route('/chat_room/<room_id>')
@login_required
def chat_room(room_id):

    client_user = str(current_user)[6:]

    tz = timezone('EST')
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %m/%d/%Y")

    users = room_id.split("_")
    for n in users:
        if n != client_user:
            user2 = n

    # get a list of dictionaries containing the columns of message table for the chat room
    message_list = []
    message_query = db.session.query(Message).filter(Message.chatroom == room_id).all()
    for message in message_query:
        message_dict = message.__dict__
        del message_dict['_sa_instance_state']
        message_list.append(message_dict)

    # create a dictionary that maps user id to username
    user1 = User.query.filter_by(username=client_user).first()
    user2_obj = User.query.filter_by(username=user2).first()
    name_to_id = {client_user: user1.id, user2: user2_obj.id}

    return render_template('chatRoom.html', time=time, username=client_user, user2=user2, room=room_id, message_hist=message_list, name_to_id=name_to_id)


def message_received():
    print("message received")


@socketio.on('message')
def message(data):
    room = data['room']
    print('received message: ' + str(data))

    mess = data['message']
    timestamp = data['date']

    # get the user.id from the username
    from_user = int(str(db.session.query(User.id).filter(User.username == current_user.username).first())[1:-2])
    to_user = int(str(db.session.query(User.id).filter(User.username == data['to']).first())[1:-2])

    m = Message(message=mess, timestamp=timestamp, from_user=from_user, to_user=to_user, chatroom=room)
    db.session.add(m)
    db.session.commit()

    socketio.emit('response', data, callback=message_received, room=room)


# show that client has connected
@socketio.on('connect')
def client_connect():
    print('connected')


@socketio.on('disconnect')
def client_disconnect():
    print('disconnected')


@socketio.on('join')
def join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.send({'msg': username + " has joined the " + room + ' room'}, room=room)


@socketio.on('leave')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.send({'msg': username + " has left the " + room + ' room'}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
