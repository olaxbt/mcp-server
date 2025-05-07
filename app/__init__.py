from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from loguru import logger
import configparser
import os
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Basic configuration
    app.config['SECRET_KEY'] = config.get('DEFAULT', 'SECRET_KEY', fallback='dev-key-please-change')
    app.config['JWT_SECRET_KEY'] = config.get('DEFAULT', 'JWT_SECRET_KEY', fallback='jwt-key-please-change')
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Configure logging
    logger.add("logs/app.log", rotation="500 MB")
    
    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.attachment_routes import attachment_bp
    from app.routes.swagger_routes import swagger_bp
    from app.routes.walletconnect_routes import walletconnect_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attachment_bp, url_prefix='/attachment')
    app.register_blueprint(swagger_bp, url_prefix='/swagger')
    app.register_blueprint(walletconnect_bp, url_prefix='/walletconnect')
    
    return app 