from flask import Flask, render_template, jsonify, request
import sqlite3


app = Flask(__name__)


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
    hospitacja = query_db("SELECT * FROM hospitacje WHERE id_hospitacji = ?", (id,), one=True)
    protokol = query_db("SELECT zawartosc_protokolu FROM hospitacje WHERE id_hospitacji = ?", (id,), one=True)
    return render_template('zatwierdzenie-hospitacji.html', hospitacja=hospitacja, protokol=protokol)


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