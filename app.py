from flask import Flask, request, jsonify, send_from_directory, render_template
import jwt
import datetime
import json
import os
import hashlib
import random
import string
import redis
import paho.mqtt.client as mqtt
from mockredis import MockRedis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

#Added MockRedis to see if that works for testing
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_client.ping()
except (redis.ConnectionError, redis.TimeoutError):
    redis_client = MockRedis()

# Load configuration from JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Load user data from JSON file
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)['users']

# Save user data to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump({'users': users}, f, indent=4)

# Generate a random string
def generate_random_string(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Serve static content
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Create new user
@app.route('/api/v1/auth/create', methods=['POST'])
def create_user():
    user_data = request.get_json()
    users = load_users()
    if any(u['username'] == user_data['username'] for u in users):
        return jsonify({'message': 'Username already exists'}), 400

    new_user = {
        'userid': max(u['userid'] for u in users) + 1 if users else 1,
        'username': user_data['username'],
        'password_hash': user_data['password_hash'],
        'seed': user_data['seed']
    }
    users.append(new_user)
    save_users(users)
    return jsonify({'message': 'User created successfully'}), 201

# Authentication challenge request
@app.route('/api/v1/auth/request', methods=['POST'])
def auth_request():
    auth_data = request.get_json()
    users = load_users()
    user = next((u for u in users if u['username'] == auth_data['username']), None)
    if user:
        session_id = generate_random_string(32)
        challenge = generate_random_string(32)
        session_data = {
            'userid': user['userid'],
            'challenge': challenge,
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        redis_client.set(session_id, json.dumps(session_data))
        return jsonify({'session_id': session_id, 'seed': user['seed'], 'challenge': challenge})
    return jsonify({'message': 'Invalid username'}), 401

# Authentication response
@app.route('/api/v1/auth/response', methods=['POST'])
def auth_response():
    auth_data = request.get_json()
    session_id = auth_data['session_id']
    session_data = redis_client.get(session_id)
    if not session_data:
        return jsonify({'message': 'Invalid session'}), 401

    session_data = json.loads(session_data)
    users = load_users()
    user = next((u for u in users if u['userid'] == session_data['userid']), None)
    if user:
        password_hash = user['password_hash']
        challenge_response = hashlib.sha256((password_hash + session_data['challenge']).encode()).hexdigest()
        if challenge_response == auth_data['challenge_response']:
            token = jwt.encode({
                'user': user['username'],
                'userid': user['userid'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config['jwt']['tokenLifetime'])
            }, app.config['SECRET_KEY'], algorithm='HS256')
            token_data = {
                'userid': user['userid'],
                'created_at': datetime.datetime.utcnow().isoformat(),
                'last_used': datetime.datetime.utcnow().isoformat()
            }
            redis_client.set(token, json.dumps(token_data))
            redis_client.delete(session_id)
            return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Middleware to update token last used time and check expiration
@app.before_request
def update_token_last_used():
    if request.endpoint in ['protected']:
        token = request.headers.get('Authorization')
        if token:
            token_data = redis_client.get(token)
            if token_data:
                token_data = json.loads(token_data)
                created_at = datetime.datetime.fromisoformat(token_data['created_at'])
                last_used = datetime.datetime.fromisoformat(token_data['last_used'])
                now = datetime.datetime.now(datetime.timezone.utc)

                # Check token lifetime
                if (now - created_at).total_seconds() > config['jwt']['tokenLifetime']:
                    redis_client.delete(token)
                    return jsonify({'message': 'Token has expired due to lifetime limit'}), 401

                # Check token expiration
                if (now - last_used).total_seconds() > config['jwt']['tokenExpiration']:
                    redis_client.delete(token)
                    return jsonify({'message': 'Token has expired due to inactivity'}), 401

                # Update last used time
                token_data['last_used'] = now.isoformat()
                redis_client.set(token, json.dumps(token_data))

# Protected API example
@app.route('/api/v1/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid!'}), 401
    return jsonify({'message': 'This is a protected route.', 'user': data['user'], 'userid': data['userid']})

# Unlock API
@app.route('/api/v1/unlock', methods=['POST'])
def unlock():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid!'}), 401

    # Connect to the local MQTT server and send the "unlock" message
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.publish("opensesame", "unlock")
    client.disconnect()

    return jsonify({'message': 'Unlock command sent successfully.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)