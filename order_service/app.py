from flask import Flask, request, jsonify
import requests
import mysql.connector
import sys, os
sys.path.append(os.path.dirname(__file__))
from db import get_db_connection
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["https://our-fashion-net.vercel.app"])

PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'https://fashion-product-service-b7atcad9dfe8g5e3.southeastasia-01.azurewebsites.net')
USER_SERVICE_URL    = os.environ.get('USER_SERVICE_URL',    'https://fashion-user-service-audqffe9dve4dscm.southeastasia-01.azurewebsites.net')
PAYMENT_SERVICE_URL = os.environ.get('PAYMENT_SERVICE_URL', 'https://fashion-payment-service-hhfghcg8bya6fvd9.southeastasia-01.azurewebsites.net')

@app.route("/")
def home():
    return "Order Service is Running"

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    cart = data.get('cart')

    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    # Step 1 — User check (User Service se)
    try:
        user_resp = requests.get(
            f"{USER_SERVICE_URL}/api/users/{customer_id}",
            timeout=5
        )
        if user_resp.status_code != 200:
            return jsonify({'error': 'User not found'}), 404
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'User service unreachable'}), 503

    # Step 2 — Stock check (Product Service se)
    for item in cart:
        product_id = item['product_id']
        quantity   = item.get('quantity', 1)
        try:
            stock_resp = requests.get(
                f"{PRODUCT_SERVICE_URL}/api/products/{product_id}/stock",
                timeout=5
            )
            stock_data = stock_resp.json()
        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Product service unreachable'}), 503

        if not stock_data.get('in_stock'):
            return jsonify({'error': f"Product {product_id} out of stock"}), 409
        if stock_data['quantity'] < quantity:
            return jsonify({'error': f"Not enough stock for product {product_id}"}), 409

    # Step 3 — Stock deduct
    for item in cart:
        requests.post(
            f"{PRODUCT_SERVICE_URL}/api/products/{item['product_id']}/deduct",
            json={'quantity': item.get('quantity', 1)},
            timeout=5
        )

    # Step 4 — Payment (Payment Service se)
    try:
        pay_resp = requests.post(
            f"{PAYMENT_SERVICE_URL}/api/payment/process",
            json={'customer_id': customer_id, 'cart': cart},
            timeout=5
        )
        pay_data = pay_resp.json()
        if not pay_data.get('success'):
            return jsonify({'error': 'Payment failed'}), 402
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Payment service unreachable'}), 503

    # Step 5 — Order save karo apne DB mein
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        for item in cart:
            qty = int(item.get('quantity', 1))
            # Jitni quantity hai, utni dafa loop chalayen aur database mein row insert karein
            for _ in range(qty):
                cursor.execute(
                    "INSERT INTO order_history (customer_id, product_id, order_date) VALUES (%s, %s, NOW())",
                    (customer_id, item['product_id'])
                )
        connection.commit()
        return jsonify({'success': True, 'message': 'Order placed successfully!'}), 201
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/orders', methods=['GET'])
def get_orders():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM order_history")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        connection.close()

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM order_history WHERE order_id = %s", (order_id,))
        connection.commit()
        return jsonify({'success': True}), 200
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)