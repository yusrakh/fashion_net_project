# Line 1 — yeh change karo
from flask import Flask, render_template, request, jsonify, session, redirect
import requests
import os

app = Flask(__name__, 
    template_folder='.',
    static_folder='static')

app.secret_key = "12345678"

# Azure Service URLs
USER_SERVICE    = 'https://fashion-user-service-audqffe9dve4dscm.southeastasia-01.azurewebsites.net'
PRODUCT_SERVICE = 'https://fashion-product-service-b7atcad9dfe8g5e3.southeastasia-01.azurewebsites.net'
ORDER_SERVICE   = 'https://fashion-order-service-gxgugehgfshngyc9.southeastasia-01.azurewebsites.net'
PAYMENT_SERVICE = 'https://fashion-payment-service-hhfghcg8bya6fvd9.southeastasia-01.azurewebsites.net'

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            resp = requests.post(
                f"{USER_SERVICE}/api/login",
                json={'email': email, 'password': password},
                timeout=10
            )
            data = resp.json()
            if data.get('success'):
                session['customer_id'] = data['customer_id']
                session['username'] = data['username']
                return render_template('login.html', 
                    message=f"Welcome {data['username']}!", 
                    success=True)
            else:
                return render_template('login.html', 
                    error="Invalid email or password.")
        except Exception as e:
            return render_template('login.html', 
                error="Service unavailable.")
    return render_template('login.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            return render_template('signup.html', 
                error="Passwords do not match.")
        try:
            resp = requests.post(
                f"{USER_SERVICE}/api/signup",
                json={'username': username, 
                      'email': email, 
                      'password': password},
                timeout=10
            )
            data = resp.json()
            if data.get('success'):
                return render_template('signup.html', success=True)
            else:
                return render_template('signup.html', 
                    error=data.get('error', 'Signup failed'))
        except Exception as e:
            return render_template('signup.html', 
                error="Service unavailable.")
    return render_template('signup.html')

# Checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_id = session.get('customer_id', 0)
        cart = request.json.get('cart', [])
        try:
            resp = requests.post(
                f"{ORDER_SERVICE}/api/orders",
                json={'customer_id': customer_id, 'cart': cart},
                timeout=10
            )
            return jsonify(resp.json()), resp.status_code
        except Exception as e:
            return jsonify({'error': 'Order service unavailable'}), 503
    return render_template('checkout.html')

# Other pages
@app.route('/brand')
def brand():
    return render_template('brand.html')

@app.route('/category')
def category():
    return render_template('category.html')



@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "fashionnet" and password == "fashion_net":
            session['admin_logged_in'] = True
            return redirect('/admin')
        return render_template('admin_login.html', 
            error="Invalid credentials.")
    return render_template('admin_login.html')

@app.route('/admin')
def admin_page():
    if 'admin_logged_in' not in session:
        return redirect('/admin_login')
    try:
        customers = requests.get(
            f"{USER_SERVICE}/api/customers", timeout=10).json()
        products = requests.get(
            f"{PRODUCT_SERVICE}/api/products", timeout=10).json()
        orders = requests.get(
            f"{ORDER_SERVICE}/api/orders", timeout=10).json()
        return render_template('admin.html',
            customers=customers,
            products=products,
            orders=orders)
    except Exception as e:
        return f"Service error: {str(e)}", 500

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin_login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)