from flask import Blueprint, request, jsonify
from services.szablon_service import get_szablon, save_szablon

szablon_bp = Blueprint('szablon', __name__)

@szablon_bp.route('/api/szablon', methods=['GET'])
def get_szablon_endpoint():
    return jsonify(get_szablon())

@szablon_bp.route('/api/szablon', methods=['POST'])
def post_szablon_endpoint():
    message, status_code = save_szablon(request.get_json())
    return jsonify(message), status_code