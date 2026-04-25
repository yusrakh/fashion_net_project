from flask import Flask, request, jsonify
import mysql.connector
import sys, os
sys.path.append(os.path.dirname(__file__))
from db import get_db_connection

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_all_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()

@app.route('/api/products/<int:product_id>/stock', methods=['GET'])
def check_stock(product_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT product_id, product_name, quantity, price FROM products WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        product['in_stock'] = product['quantity'] > 0
        return jsonify(product), 200
    finally:
        cursor.close()
        connection.close()

@app.route('/api/products/<int:product_id>/deduct', methods=['POST'])
def deduct_stock(product_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE products SET quantity = quantity - %s WHERE product_id = %s AND quantity >= %s",
            (quantity, product_id, quantity)
        )
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Not enough stock'}), 400
        return jsonify({'success': True}), 200
    finally:
        cursor.close()
        connection.close()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()
        return jsonify({'success': True}), 200
    finally:
        cursor.close()
        connection.close()

# ─── Brand specific tables ────────────────────────
BRAND_TABLES = {
    'ethnic':     'ethnic_products',
    'zellbury':   'zellbury_products',
    'sapphire':   'sapphire_products',
    'outfitters': 'outfitter_products',
    'saya':       'saya_products',
}

@app.route('/api/brands/<brand_name>/products', methods=['GET'])
def get_brand_products(brand_name):
    table = BRAND_TABLES.get(brand_name.lower())
    if not table:
        return jsonify({'error': 'Brand not found'}), 404
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {table}")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)