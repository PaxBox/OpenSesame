import hashlib
import requests
import json
import random
import string

# Function to create a new user
def create_user(username, password):
    # Generate seed and password hash
    seed = generate_random_string(16)
    password_hash = hashlib.sha256((password + seed).encode()).hexdigest()

    user_data = {
        "username": username,
        "password_hash": password_hash,
        "seed": seed
    }
    response = requests.post('http://127.0.0.1:5000/api/v1/auth/create', json=user_data)
    if response.status_code == 201:
        print("User created successfully")
    else:
        print("Failed to create user:", response.json())

# Function to generate a random string
def generate_random_string(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Function to authenticate and get a token
def authenticate(username, password):
    # Step 1: Request authentication challenge
    auth_request_data = {
        "username": username
    }

    response = requests.post('http://127.0.0.1:5000/api/v1/auth/request', json=auth_request_data)
    if response.status_code != 200:
        print("Failed to get authentication challenge:", response.json())
        return None

    response_data = response.json()
    session_id = response_data['session_id']
    seed = response_data['seed']
    challenge = response_data['challenge']

    # Step 2: Generate challenge response
    password_hash = hashlib.sha256((password + seed).encode()).hexdigest()
    challenge_response = hashlib.sha256((password_hash + challenge).encode()).hexdigest()

    auth_response_data = {
        "session_id": session_id,
        "challenge_response": challenge_response
    }

    # Step 3: Authenticate with the challenge response
    response = requests.post('http://127.0.0.1:5000/api/v1/auth/response', json=auth_response_data)
    if response.status_code != 200:
        print("Authentication failed:", response.json())
        return None

    token = response.json()['token']
    print("Authentication successful, token:", token)
    return token

# Function to access the protected route using the token
def access_protected_route(token):
    headers = {
        "Authorization": token
    }

    response = requests.get('http://127.0.0.1:5000/api/v1/protected', headers=headers)
    if response.status_code != 200:
        print("Failed to access protected route:", response.json())
        return

    print("Protected route response:", response.json())

# Example usage
create_user("new_user", "new_password")
token = authenticate("new_user", "new_password")
if token:
    access_protected_route(token)