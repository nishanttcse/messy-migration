# app/routes/users.py
#this module defines routes for user management in a Flask application.
# It includes endpoints for creating, retrieving, updating, and deleting users,
# as well as user authentication and searching for users by name.
# The routes are organized using Flask's Blueprint feature for better modularity.


from flask import Blueprint, request, jsonify
from app.models import user_model
from app.utils.security import hash_password, check_password

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'User Management API'}), 200

@user_routes.route('/users', methods=['GET'])
def get_users():
    try:
        users = user_model.get_all_users()
        # Do not return passwords
        for user in users:
            user.pop('password', None)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Missing name, email, or password'}), 400

    hashed = hash_password(password)
    try:
        user_model.create_user(name, email, hashed)
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not all([name, email]):
        return jsonify({'error': 'Missing name or email'}), 400

    try:
        user_model.update_user(user_id, name, email)
        return jsonify({'message': 'User updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_model.delete_user(user_id)
        return jsonify({'message': f'User {user_id} deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/search', methods=['GET'])
def search_user():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing name parameter'}), 400

    try:
        users = user_model.search_users(name)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400

    user = user_model.get_user_by_email(email)
    if user and check_password(password, user['password']):
        return jsonify({'status': 'success', 'user_id': user['id']}), 200

    return jsonify({'status': 'failed', 'error': 'Invalid credentials'}), 401
