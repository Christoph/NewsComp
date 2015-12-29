# -*- coding: utf-8 -*-

import socketio
import eventlet
from flask import Flask

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('my message')
def message(sid, data):
    print('message ', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
