import json
from flask import jsonify

def get_szablon():
    with open('szablon.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_szablon(request):
    try:
        if not request.is_json:
            return jsonify({"error": "Dane muszą być w formacie JSON"}), 400

        new_szablon = request.get_json()

        with open('szablon.json', 'w', encoding='utf-8') as file:
            json.dump(new_szablon, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Szablon został zapisany pomyślnie"}), 201
    except Exception as e:
        return jsonify({"error": f"Coś poszło nie tak: {str(e)}"}), 500