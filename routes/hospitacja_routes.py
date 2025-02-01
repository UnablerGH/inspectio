from flask import Blueprint, jsonify
from services.hospitacja_service import get_hospitacje_pracownika, get_hospitacja_details, zaakceptuj_hospitacje

hospitacja_bp = Blueprint('hospitacje', __name__)

@hospitacja_bp.route('/api/hospitacje/<int:id_pracownika>', methods=['GET'])
def get_hospitacje(id_pracownika):
    return jsonify(get_hospitacje_pracownika(id_pracownika))

@hospitacja_bp.route('/api/hospitacja/<int:id_hospitacji>', methods=['GET'])
def get_hospitacja_endpoint(id_hospitacji):
    hospitacja = get_hospitacja_details(id_hospitacji)
    if not hospitacja:
        return jsonify({'error': 'Hospitacja not found'}), 404
    return jsonify(hospitacja)

@hospitacja_bp.route('/api/hospitacja/<int:id_hospitacji>/zaakceptuj', methods=['POST'])
def zaakceptuj_hospitacje_endpoint(id_hospitacji):
    return jsonify(zaakceptuj_hospitacje(id_hospitacji)), 200