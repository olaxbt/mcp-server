from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
import os
import uuid
from flasgger import swag_from

# Blueprint for attachment routes
attachment_bp = Blueprint('attachment', __name__)

UPLOAD_FOLDER = 'upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@attachment_bp.route('/upload', methods=['POST'])
@jwt_required()
@swag_from({
    'responses': {
        201: {
            'description': 'File uploaded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'file_id': {
                        'type': 'string'
                    }
                }
            }
        },
        400: {
            'description': 'No file part or no selected file'
        }
    }
})
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    file.save(file_path)
    return jsonify({'file_id': file_id}), 201

@attachment_bp.route('/file/<file_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'parameters': [
        {
            'name': 'file_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'UUID of the file to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'File retrieved successfully'
        },
        404: {
            'description': 'File not found'
        }
    }
})
def get_file(file_id):
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path)