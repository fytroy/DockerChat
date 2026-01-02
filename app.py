import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/instance/chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Use simple in-memory mode for single server, or Redis for multi-server
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=False)

# Ensure instance directory exists
import os
os.makedirs('/app/instance', exist_ok=True)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image, video, link
    room = db.Column(db.String(50), default='general')
    is_private = db.Column(db.Boolean, default=False)
    recipient = db.Column(db.String(80), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()
    # Create default rooms if they don't exist
    if Room.query.count() == 0:
        default_rooms = [
            Room(name='general', description='General discussion'),
            Room(name='random', description='Random chat'),
            Room(name='tech', description='Technology discussion'),
            Room(name='gaming', description='Gaming chat')
        ]
        for room in default_rooms:
            db.session.add(room)
        db.session.commit()

# Store active users {session_id: {username, room}}
active_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rooms')
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{'name': r.name, 'description': r.description} for r in rooms])

@app.route('/api/messages/<room_name>')
def get_messages(room_name):
    messages = Message.query.filter_by(room=room_name, is_private=False).order_by(Message.timestamp.desc()).limit(50).all()
    return jsonify([{
        'username': m.username,
        'content': m.content,
        'message_type': m.message_type,
        'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for m in reversed(messages)])

@app.route('/api/users')
def get_users():
    users = list(set([u['username'] for u in active_users.values()]))
    return jsonify(users)

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data.get('room', 'general')
    
    # Store user info
    active_users[request.sid] = {'username': username, 'room': room}
    
    # Add user to database if new
    if not User.query.filter_by(username=username).first():
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
    
    # Join the room
    join_room(room)
    
    # Notify others
    emit('user_joined', {
        'username': username,
        'message': f'{username} joined {room}',
        'users': list(set([u['username'] for u in active_users.values() if u['room'] == room]))
    }, room=room)
    
    print(f'User {username} joined room {room}')

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data.get('room', 'general')
    
    leave_room(room)
    
    # Notify others
    emit('user_left', {
        'username': username,
        'message': f'{username} left {room}'
    }, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data.get('room', 'general')
    message_type = data.get('type', 'text')
    
    # Save message to database
    new_message = Message(
        username=username,
        content=message,
        message_type=message_type,
        room=room
    )
    db.session.add(new_message)
    db.session.commit()
    
    # Broadcast message
    emit('message', {
        'username': username,
        'message': message,
        'type': message_type,
        'timestamp': datetime.utcnow().strftime('%H:%M')
    }, room=room)

@socketio.on('private_message')
def handle_private_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    
    # Save private message
    new_message = Message(
        username=sender,
        content=message,
        is_private=True,
        recipient=recipient
    )
    db.session.add(new_message)
    db.session.commit()
    
    # Send to recipient (find their session)
    recipient_sid = None
    for sid, user_info in active_users.items():
        if user_info['username'] == recipient:
            recipient_sid = sid
            break
    
    msg_data = {
        'sender': sender,
        'message': message,
        'timestamp': datetime.utcnow().strftime('%H:%M')
    }
    
    if recipient_sid:
        emit('private_message', msg_data, room=recipient_sid)
    
    # Send back to sender as confirmation
    emit('private_message', msg_data)

@socketio.on('typing')
def handle_typing(data):
    username = data['username']
    room = data.get('room', 'general')
    is_typing = data.get('is_typing', False)
    
    emit('user_typing', {
        'username': username,
        'is_typing': is_typing
    }, room=room, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in active_users:
        user_info = active_users[request.sid]
        username = user_info['username']
        room = user_info['room']
        
        # Remove user
        del active_users[request.sid]
        
        # Notify others
        emit('user_left', {
            'username': username,
            'message': f'{username} left the chat',
            'users': list(set([u['username'] for u in active_users.values() if u['room'] == room]))
        }, room=room)
        
        print(f'User {username} disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)