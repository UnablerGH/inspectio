import json
from flask import jsonify

def get_szablon():
    with open('szablon.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_szablon(data):
    try:
        if not isinstance(data, dict):
            raise ValueError("Dane muszą być w formacie JSON")

        with open('szablon.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return {"message": "Szablon został zapisany pomyślnie"}
    except Exception as e:
        return {"error": f"Coś poszło nie tak: {str(e)}"}