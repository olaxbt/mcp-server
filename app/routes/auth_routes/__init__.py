from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import create_access_token
import os
import uuid
from flasgger import swag_from

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def register():
    # Dummy registration logic
    username = request.json.get('username')
    password = request.json.get('password')
    # Here you would add logic to store the user in a database
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'User logged in successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def login():
    # Dummy login logic
    username = request.json.get('username')
    password = request.json.get('password')
    # Here you would add logic to verify the user
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
