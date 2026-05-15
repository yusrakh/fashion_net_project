from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import sys, os
sys.path.append(os.path.dirname(__file__))
from db import get_db_connection

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user['password'] == password:
            return jsonify({
                'success': True,
                'customer_id': user['customer_id'],
                'username': user['username']
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        connection.close()

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 409
        cursor.execute(
            "INSERT INTO customers (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        connection.commit()
        return jsonify({'success': True, 'message': 'User registered'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/users/<int:customer_id>', methods=['GET'])
def get_user(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT customer_id, username, email FROM customers WHERE customer_id = %s",
            (customer_id,)
        )
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    finally:
        cursor.close()
        connection.close()

@app.route('/api/customers', methods=['GET'])
def get_all_customers():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT customer_id, username, email FROM customers")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        connection.commit()
        return jsonify({'success': True}), 200
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)