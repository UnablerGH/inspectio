from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to query the database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# API to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = query_db('SELECT * FROM users')
    return jsonify([dict(user) for user in users])

# API to add a user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
