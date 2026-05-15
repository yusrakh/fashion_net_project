# from flask import Flask, render_template, request, redirect, url_for, session
# from db import get_db_connection
# from werkzeug.security import generate_password_hash, check_password_hash
# import mysql.connector
# from db import get_db_connection

# app = Flask(__name__)
# app.secret_key = "12345678"  # Use environment variables for sensitive keys in production

# # Dummy admin credentials
# ADMIN_USERNAME = "fashionnet"
# ADMIN_PASSWORD = "fashion_net"

# # Add Order
# @app.route('/admin/order_history/add', methods=['POST'])
# def add_order():
#     if 'admin_logged_in' in session:
#         customer_id = request.form['customer_id']
#         product_id = request.form['product_id']
#         order_date = request.form['order_date']

#         connection = get_db_connection()
#         cursor = connection.cursor()

#         try:
#             # Validate customer_id and product_id
#             cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
#             if not cursor.fetchone():
#                 return "Customer ID not found!", 400

#             cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
#             if not cursor.fetchone():
#                 return "Product ID not found!", 400

#             # Insert order
#             cursor.execute(
#                 "INSERT INTO order_history (customer_id, product_id, order_date) VALUES (%s, %s, %s)",
#                 (customer_id, product_id, order_date)
#             )
#             connection.commit()
#             return redirect(url_for('admin_page'))
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))
    

# @app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
# def delete_product(product_id):
#     if 'admin_logged_in' in session:  # Ensure the admin is logged in
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         try:
#             # Delete the product from the database
#             cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
#             connection.commit()
#             return redirect(url_for('admin_page'))  # Redirect to admin dashboard after deletion
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))  # Redirect to admin login if not logged in

# @app.route('/order_history')
# def order_history():
#     query = '''
#         SELECT 
#             oh.order_id,
#             oh.customer_id,
#             c.username AS customer_name,
#             p.product_id,
#             p.product_name,
#             p.price,
#             p.product_type,
#             oh.order_date
#         FROM 
#             order_history oh
#         JOIN 
#             products p ON oh.product_id = p.product_id
#         JOIN 
#             customers c ON oh.customer_id = c.customer_id;
#     '''
#     orders = db.execute(query).fetchall()
#     return render_template('order_history.html', orders=orders)


# @app.route('/admin/order_history/delete/<int:order_id>', methods=['POST'])
# def delete_order(order_id):
#     if 'admin_logged_in' in session:  # Ensure the admin is logged in
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         try:
#             # Delete the order based on the order ID
#             cursor.execute("DELETE FROM order_history WHERE order_id = %s", (order_id,))
#             connection.commit()
#             return redirect(url_for('admin_page'))
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))

# @app.route('/admin/brands/delete/<int:brand_id>', methods=['POST'])
# def delete_brand(brand_id):
#     if 'admin_logged_in' in session:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         try:
#             cursor.execute("DELETE FROM brands WHERE brand_id = %s", (brand_id,))
#             connection.commit()
#             return redirect(url_for('admin_page'))
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))
# @app.route('/admin/customers/delete/<int:customer_id>', methods=['POST'])
# def delete_customer(customer_id):
#     if 'admin_logged_in' in session:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         try:
#             cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
#             connection.commit()
#             return redirect(url_for('admin_page'))
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))


# @app.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Hard-coded admin credentials
#         if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#             session['admin_logged_in'] = True
#             return redirect(url_for('admin_page'))  # Redirect to the admin dashboard
#         else:
#             return render_template('admin_login.html', error="Invalid admin credentials.")

#     return render_template('admin_login.html')



# @app.route('/admin', methods=['GET'])
# def admin_page():
#     if 'admin_logged_in' in session:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             # Fetch customers
#             cursor.execute("SELECT * FROM customers")
#             customers = cursor.fetchall()

#             # Fetch brands
#             cursor.execute("SELECT * FROM brands")
#             brands = cursor.fetchall()

#             # Fetch all products and group them by brand
#             cursor.execute("""
#                 SELECT 
#                     b.brand_name, 
#                     p.product_id, 
#                     p.product_name, 
#                     p.product_type, 
#                     p.price, 
#                     p.quantity, 
#                     p.description 
#                 FROM products p
#                 JOIN brands b ON p.brand_id = b.brand_id
#             """)
#             raw_brand_products = cursor.fetchall()

#             # Group products by brand
#             brand_products = {}
#             for product in raw_brand_products:
#                 brand_name = product.pop("brand_name")
#                 if brand_name not in brand_products:
#                     brand_products[brand_name] = []
#                 brand_products[brand_name].append(product)

#             # Fetch order history
#             cursor.execute("""
#                 SELECT 
#                     oh.order_id, 
#                     oh.customer_id, 
#                     c.username AS customer_name, 
#                     oh.product_id, 
#                     p.product_name, 
#                     p.price, 
#                     p.product_type, 
#                     oh.order_date
#                 FROM order_history oh
#                 JOIN customers c ON oh.customer_id = c.customer_id
#                 JOIN products p ON oh.product_id = p.product_id
#             """)
#             order_history = cursor.fetchall()

#             # Render the admin page
#             return render_template(
#                 'admin.html',
#                 customers=customers,
#                 brands=brands,
#                 brand_products=brand_products,
#                 order_history=order_history
#             )
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return redirect(url_for('admin_login'))



# @app.route('/checkout', methods=['POST'])
# def process_checkout():
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         # If the customer is logged in, fetch their ID; otherwise, assign a guest customer ID (e.g., 0)
#         customer_id = session.get('customer_id', 0)  # Default to 0 for guest users

#         # Get cart data from the request
#         cart = request.json.get('cart')  # Assume cart is sent as a JSON object

#         if not cart or len(cart) == 0:
#             return jsonify({'error': 'Cart is empty!'}), 400

#         for item in cart:
#             product_id = item['product_id']
#             quantity = item['quantity']

#             # Fetch product details to validate and retrieve relevant data
#             cursor.execute("SELECT product_name, quantity FROM products WHERE product_id = %s", (product_id,))
#             product = cursor.fetchone()

#             if not product:
#                 return jsonify({'error': f'Product ID {product_id} does not exist!'}), 404
#             if product['quantity'] < quantity:
#                 return jsonify({'error': f'Not enough stock for Product ID {product_id}!'}), 400

#             # Deduct stock
#             cursor.execute(
#                 "UPDATE products SET quantity = quantity - %s WHERE product_id = %s",
#                 (quantity, product_id)
#             )

#             # Insert order into order_history
#             cursor.execute(
#                 """
#                 INSERT INTO order_history (customer_id, product_id, order_date)
#                 VALUES (%s, %s, NOW())
#                 """,
#                 (customer_id, product_id)
#             )

#         # Commit the transaction
#         connection.commit()
#         return jsonify({'success': 'Order placed successfully and recorded in order_history!'}), 200

#     except mysql.connector.Error as err:
#         connection.rollback()
#         return jsonify({'error': f'Database Error: {str(err)}'}), 500

#     finally:
#         cursor.close()
#         connection.close()




# # Home Page Route
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             # Check if the user exists in the database
#             cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
#             user = cursor.fetchone()

#             # Directly compare the password
#             if user and user['password'] == password:
#                 session['customer_id'] = user['customer_id']
#                 return render_template('login.html', message="Login successful!", success=True)
#             else:
#                 return render_template('login.html', error="Invalid email or password.")
#         finally:
#             cursor.close()
#             connection.close()

#     return render_template('login.html')






# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm-password')

#         if not username or not email or not password or not confirm_password:
#             return render_template('signup.html', error="All fields are required.")

#         if password != confirm_password:
#             return render_template('signup.html', error="Passwords do not match.")

#         # Do not hash the password (storing plain text)
#         plain_password = password

#         connection = get_db_connection()
#         cursor = connection.cursor()

#         try:
#             cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
#             if cursor.fetchone():
#                 return render_template('signup.html', error="Email is already registered.")

#             # Store the plain password
#             cursor.execute(
#                 "INSERT INTO customers (username, email, password) VALUES (%s, %s, %s)",
#                 (username, email, plain_password)
#             )
#             connection.commit()
#             return render_template('signup.html', success=True)
#         except mysql.connector.Error as err:
#             return render_template('signup.html', error=f"Database Error: {err}")
#         finally:
#             cursor.close()
#             connection.close()

#     return render_template('signup.html')



# # Other Routes
# @app.route('/category')
# def category():
#     return render_template('category.html')


# @app.route('/brand')
# def brand():
#     return render_template('brand.html')


# @app.route('/checkout')
# def checkout():
#     return render_template('checkout.html')


# @app.route('/blog')
# def blog():
#     return render_template('blog.html')

# @app.route('/admin/logout', methods=['GET'])
# def admin_logout():
#     # Remove the admin session
#     session.pop('admin_logged_in', None)
#     return redirect(url_for('admin_login'))


# if __name__ == '__main__':
#     app.run(debug=True)
