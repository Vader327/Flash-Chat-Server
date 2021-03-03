from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms
import socket
#import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "f34c5d6e1a43408dbbac6adb6baacbd9"
socketio = SocketIO(app)

#url_to_connect = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]



@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("index.html")
  
  elif request.method == "POST":
    session['username'] = request.form['username']
    session['room'] = request.form['room']
    return redirect(url_for('chat'))



@app.route('/chat')
def chat(methods=['GET', 'POST']):
  username = session.get('username')
  room = session.get('room')
  if username and room:
    data = {'username': username, 'room': room}
    return render_template("chat.html", data=data)
  else:
    return redirect(url_for('login'))



@socketio.on('join', namespace='/chat')
def join():
  client_room = session.get('room')
  join_room(client_room, namespace='/chat')
  emit('status', {'username': session.get('username'), 'type': 'join'}, namespace='/chat', room=client_room)
  


@socketio.on('leave', namespace='/chat')
def leave():
  client_room = session.get('room')
  leave_room(client_room, namespace='/chat')
  emit('status', {'username': session.get('username'), 'type': 'leave'}, namespace='/chat', room=client_room)



@socketio.on('send message', namespace='/chat')
def send_message(json):
  emit('receive message', json, namespace='/chat', room=session.get('room'))



"""
@socketio.on('fetch_participants', namespace='/chat')
def fetch_participants(methods=['GET', 'POST']):
  socketio.emit('return_participants', namespace='/chat')
  
"""
  
if __name__ == "__main__":
  #socketio.run(app, debug=True, host=url_to_connect)
  socketio.run(app, debug=True)
