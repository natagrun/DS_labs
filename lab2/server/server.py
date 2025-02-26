from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)


DB_CONFIG = {
    'dbname': 'users',
    'user': 'server',
    'password': 'server',
    'host': 'localhost',
    'port': '5432'
}


def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


@app.route('/persons', methods=['GET'])
def get_persons():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM person;')
    persons = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(persons)


@app.route('/persons', methods=['POST'])
def add_person():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    age = data['age']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            sql.SQL('INSERT INTO person (name, surname, email, age) VALUES (%s, %s, %s, %s);'),
            (name, surname, email, age)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Person added successfully!'}), 201
    except psycopg2.IntegrityError as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': 'Email already exists!'}), 400
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)