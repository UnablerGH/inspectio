from flask import Blueprint, jsonify, request
from services.hospitacja_service import get_hospitacje_pracownika, get_hospitacja_details, zaakceptuj_hospitacje, get_zlecone_hospitacje, update_hospitacja_protocol
from services.szablon_service import get_szablon, save_szablon

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


@hospitacja_bp.route('/api/hospitacje/zlecone/<int:id_pracownika>', methods=['GET'])
def get_zlecone_hospitacje_endpoint(id_pracownika):
    hospitacje = get_zlecone_hospitacje(id_pracownika)
    if not hospitacje:
        return jsonify({'error': 'Brak zleconych hospitacji dla pracownika'}), 404
    return jsonify(hospitacje)

@hospitacja_bp.route('/api/hospitacja/<int:id_hospitacji>/zapisz', methods=['POST'])
def zapisz_hospitacje_protocol_endpoint(id_hospitacji):
    data = request.get_json()
    print("Otrzymane dane:", data)
    new_protocol = data.get('protocol')
    if new_protocol is None:
        return jsonify({"error": "Brak protokołu w żądaniu"}), 400
    result = update_hospitacja_protocol(id_hospitacji, new_protocol)
    return jsonify(result), 200


@hospitacja_bp.route('/api/szablon', methods=['GET'])
def get_szablon_endpoint():
    try:
        szablon = get_szablon()
        return jsonify(szablon)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hospitacja_bp.route('/api/szablon', methods=['POST'])
def save_szablon_endpoint():
    data = request.get_json()
    result, status = save_szablon(data)
    return jsonify(result), status