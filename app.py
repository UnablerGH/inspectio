import json
from flask import Flask, render_template, jsonify, request
import sqlite3


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
    return (rv[0] if rv else None) if one else rv

# Strony
@app.route('/')
def dziekan_menu():
    return render_template('dziekan-menu.html')


@app.route('/edycja-szablonu')
def edycja_szablonu():
    return render_template('edycja-szablonu.html')


@app.route('/menu')
def hospitacje_menu():
    return render_template('hospitacje-menu.html')


@app.route('/dotyczace-mnie')
def hospitacje_dotyczace_mnie():
    return render_template('hospitacje-dotyczace-mnie.html')

@app.route('/zlecone-mi')
def hospitacje_zlecone_mi():
    return render_template('zlecone-hospitacje.html')

@app.route('/zatwierdzenie-hospitacji/<int:id>')
def zatwierdzenie_hospitacji(id):
    return render_template('zatwierdzenie-hospitacji.html', id=id)


# Operacje
@app.route('/api/szablon', methods=['GET'])
def get_szablon():
    with open('szablon.json', 'r', encoding='utf-8') as file:
        szablon = json.load(file) 
    return jsonify(szablon)

@app.route('/api/szablon', methods=['POST'])
def post_szablon():
    try:
        if not request.is_json:
            return jsonify({"error": "Dane muszą być w formacie JSON"}), 400

        new_szablon = request.get_json()

        with open('szablon.json', 'w', encoding='utf-8') as file:
            json.dump(new_szablon, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Szablon został zapisany pomyślnie"}), 201
    except Exception as e:
        return jsonify({"error": f"Coś poszło nie tak: {str(e)}"}), 500
    
@app.route('/api/pracownik/<int:id_pracownika>', methods=['GET'])
def get_pracownik(id_pracownika):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT p.imie, p.nazwisko 
    FROM pracownicy p
    WHERE p.id_pracownika = ?
    ''', (id_pracownika,))
    
    user = cursor.fetchone() 

    conn.close()

    if user:
        return jsonify({
            'imie': user['imie'],
            'nazwisko': user['nazwisko']
        })
    else:
        return jsonify({"error": "Użytkownik nie znaleziony"}), 404
    
@app.route('/api/hospitacje/<int:id_pracownika>', methods=['GET'])
def get_hospitacje_pracownika(id_pracownika):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT h.id_hospitacji, h.termin, h.data_zatwierdzenia, p.nazwa
    FROM hospitacje h
    JOIN przedmioty p ON h.przedmiot_id = p.id_przedmiotu
    WHERE h.hospitowany_id = ? AND h.data_sporzadzenia IS NOT NULL
    ORDER BY h.termin DESC
    ''', (id_pracownika,))
    
    hospitacje = cursor.fetchall()
    conn.close()
    
    return jsonify([
        {
            'id': h['id_hospitacji'],
            'termin': h['termin'],
            'status': 'completed' if h['data_zatwierdzenia'] else 'pending',
            'nazwa': h['nazwa']
        } for h in hospitacje
    ])

@app.route('/api/hospitacja/<int:id_hospitacji>', methods=['GET'])
def get_hospitacja_details(id_hospitacji):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT 
        p.nazwa AS przedmiot_nazwa,
        p.kod AS przedmiot_kod,
        h.termin,
        h.miejsce,
        h.zawartosc_protokolu AS protokol,
        h.data_zatwierdzenia,
        GROUP_CONCAT(pracownicy.imie || ' ' || pracownicy.nazwisko) AS zespol_hospitujacy
    FROM hospitacje h
    JOIN przedmioty p ON h.przedmiot_id = p.id_przedmiotu
    LEFT JOIN zespoly_hospitujace zh ON h.id_hospitacji = zh.id_hospitacji
    LEFT JOIN pracownicy ON pracownicy.id_pracownika = zh.id_hospitujacego
    WHERE h.id_hospitacji = ?
    GROUP BY h.id_hospitacji
    '''

    cursor.execute(query, (id_hospitacji,))
    hospitacja = cursor.fetchone()
    conn.close()

    if hospitacja:
        status = 'completed' if hospitacja['data_zatwierdzenia'] else 'pending'

        return jsonify({
            'przedmiot_nazwa': hospitacja['przedmiot_nazwa'],
            'przedmiot_kod': hospitacja['przedmiot_kod'],
            'termin': hospitacja['termin'],
            'miejsce': hospitacja['miejsce'],
            'protokol': hospitacja['protokol'],
            'zespol_hospitujacy': hospitacja['zespol_hospitujacy'].split(',') if hospitacja['zespol_hospitujacy'] else [],
            'status': status
        })
    else:
        return jsonify({'error': 'Hospitacja not found'}), 404
    
@app.route('/api/hospitacja/<int:id_hospitacji>/zaakceptuj', methods=['POST'])
def zaakceptuj_hospitacje(id_hospitacji):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE hospitacje
        SET data_zatwierdzenia = CURRENT_TIMESTAMP
        WHERE id_hospitacji = ?
    ''', (id_hospitacji,))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Hospitacja została zaakceptowana'}), 200

@app.route('/api/hospitacje', methods=['GET'])
def get_hospitacje():
    hospitacje = query_db('SELECT * FROM hospitacje')
    return jsonify([dict(hospitacja) for hospitacja in hospitacje])


@app.route('/api/protokol/<int:hospitacja_id>', methods=['GET'])
def get_protokol(hospitacja_id):
    protokol = query_db('SELECT zawartosc_protokolu FROM hospitacje WHERE id_hospitacji = ?', (hospitacja_id,), one=True)
    return jsonify(protokol if protokol else {'zawartosc_protokolu': ''})


@app.route('/api/protokol/<int:hospitacja_id>', methods=['POST'])
def save_protokol(hospitacja_id):
    data = request.json
    zawartosc_protokolu = data.get('zawartosc_protokolu')
    query_db('UPDATE hospitacje SET zawartosc_protokolu = ? WHERE id_hospitacji = ?', (zawartosc_protokolu, hospitacja_id))
    return jsonify({'message': 'Protokół zapisany pomyślnie'})


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    mock_notifications = [{"id": 1, "message": "Nowe hospitacje do zatwierdzenia."},
                           {"id": 2, "message": "Zmiana terminu hospitacji."}]
    return jsonify(mock_notifications)

if __name__ == '__main__':
    app.run(debug=True)