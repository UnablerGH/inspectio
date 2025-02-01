from flask import Blueprint, jsonify
from services.pracownik_service import get_pracownik

pracownik_bp = Blueprint('pracownik', __name__)

@pracownik_bp.route('/api/pracownik/<int:id_pracownika>', methods=['GET'])
def get_pracownik_endpoint(id_pracownika):
    user = get_pracownik(id_pracownika)
    if user:
        return jsonify({
            'imie': user['imie'],
            'nazwisko': user['nazwisko']
        })
    else:
        return jsonify({"error": "Użytkownik nie znaleziony"}), 404