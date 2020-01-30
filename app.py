# server side code

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, send

# initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpassword'
socketio = SocketIO(app, cors_allowed_origins='*')


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