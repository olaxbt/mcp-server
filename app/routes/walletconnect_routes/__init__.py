from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.routes.walletconnect_routes.walletconnect_sdk import WalletConnectWrapper

# Blueprint for WalletConnect routes
walletconnect_bp = Blueprint('walletconnect', __name__)


# Initialize WalletConnect wrapper
wc_wrapper = WalletConnectWrapper()

@walletconnect_bp.route('/create_session', methods=['GET'])
def create_session():
    """
    Create a new WalletConnect session.
    ---
    tags:
      - WalletConnect
    responses:
      200:
        description: Session created successfully
    """
    try:
        uri = wc_wrapper.create_session()
        return jsonify({"status": "session created", "uri": uri}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@walletconnect_bp.route('/connect', methods=['POST'])
def connect():
    """
    Connect to a wallet.
    ---
    tags:
      - WalletConnect
    responses:
      200:
        description: Wallet connected successfully
    """
    try:
        response = wc_wrapper.connect()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@walletconnect_bp.route('/disconnect', methods=['POST'])
def disconnect():
    """
    Disconnect the wallet.
    ---
    tags:
      - WalletConnect
    responses:
      200:
        description: Wallet disconnected successfully
    """
    try:
        response = wc_wrapper.disconnect()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@walletconnect_bp.route('/status', methods=['GET'])
def session_status():
    """
    Get the current session status.
    ---
    tags:
      - WalletConnect
    responses:
      200:
        description: Current session status
    """
    try:
        status = wc_wrapper.get_session_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500