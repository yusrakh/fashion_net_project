from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    customer_id = data.get('customer_id')
    cart = data.get('cart')

    if not customer_id or not cart:
        return jsonify({'success': False, 'error': 'Missing data'}), 400

    total = sum(
        item.get('price', 100) * item.get('quantity', 1)
        for item in cart
    )

    # 90% success simulation
    if random.random() < 0.9:
        return jsonify({
            'success': True,
            'transaction_id': f"TXN-{random.randint(10000,99999)}",
            'amount': total,
            'message': 'Payment successful'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Payment declined (simulation)'
        }), 402

@app.route('/api/payment/status', methods=['GET'])
def status():
    return jsonify({'service': 'Payment Service', 'status': 'running'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)