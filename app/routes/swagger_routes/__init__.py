from flask import Blueprint, request, jsonify, send_file
from flask import render_template

# Blueprint for documentation route
swagger_bp = Blueprint('swagger', __name__)

#@doc_route.route('/api-docs', methods=['GET'])
#def api_docs():
#    return render_template('api_docs.html')

@swagger_bp.route('/')
def swagger_ui():
    """
    Swagger UI
    ---
    tags:
      - Documentation
    responses:
      200:
        description: Swagger UI
    """
    return "Swagger UI is available at /apidocs"