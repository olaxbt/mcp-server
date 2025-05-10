from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import create_access_token
import os
import uuid

# Blueprint for authentication routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    # Here you would add logic to store the user in a database
    return jsonify({'message': 'Welcome to MCP SERVER'}), 201
