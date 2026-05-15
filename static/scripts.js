// ─── Azure Service URLs ───────────────────────────
const API = {
    user:    'https://fashion-user-service-audqffe9dve4dscm.southeastasia-01.azurewebsites.net',
    product: 'https://fashion-product-service-b7atcad9dfe8g5e3.southeastasia-01.azurewebsites.net',
    order:   'https://fashion-order-service-gxgugehgfshngyc9.southeastasia-01.azurewebsites.net',
    payment: 'https://fashion-payment-service-hhfghcg8bya6fvd9.southeastasia-01.azurewebsites.net'
};

document.addEventListener('DOMContentLoaded', function () {
    console.log('Fashion.net website loaded.');

    let cart = [];

    // ─── Brand/Category Name Update ───────────────
    const brandNameElement = document.getElementById('brand-name');
    const categoryNameElement = document.getElementById('category-name');
    const params = new URLSearchParams(window.location.search);

    const capitalizeFirstLetter = (string) => string.charAt(0).toUpperCase() + string.slice(1);
    const formatCategoryName = (string) => string.split('-').map(capitalizeFirstLetter).join(' ');

    if (brandNameElement) {
        const brand = params.get('brand');
        brandNameElement.innerText = brand ? capitalizeFirstLetter(brand) : 'Unknown Brand';
    }

    if (categoryNameElement) {
        const category = params.get('category');
        categoryNameElement.innerText = category ? formatCategoryName(category) : 'Unknown Category';
    }

    // ─── SIGNUP ───────────────────────────────────
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm-password').value;

            if (password !== confirm) {
                alert('Passwords do not match!');
                return;
            }

            try {
                const resp = await fetch(`${API.user}/api/signup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });
                const data = await resp.json();
                if (data.success) {
                    alert('Signup successful! Please login.');
                    window.location.href = 'login.html';
                } else {
                    alert(data.error || 'Signup failed!');
                }
            } catch (err) {
                alert('Service unavailable. Try again.');
            }
        });
    }

    // ─── LOGIN ────────────────────────────────────
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const resp = await fetch(`${API.user}/api/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await resp.json();
                if (data.success) {
                    localStorage.setItem('customer_id', data.customer_id);
                    localStorage.setItem('username', data.username);
                    alert(`Welcome ${data.username}!`);
                    window.location.href = 'index.html';
                } else {
                    alert('Invalid email or password!');
                }
            } catch (err) {
                alert('Service unavailable. Try again.');
            }

            
        });
    }

    // ─── LOAD PRODUCTS ────────────────────────────
    const collectionGrid = document.querySelector('.collection-grid');
    if (collectionGrid) {
        fetch(`${API.product}/api/products`)
            .then(r => r.json())
            .then(products => {
                collectionGrid.innerHTML = '';
                products.forEach(product => {
                    const item = document.createElement('div');
                    item.classList.add('collection-item');
                    item.innerHTML = `
                        <h3>${product.product_name}</h3>
                        <p>Rs. ${product.price}</p>
                        <p>${product.product_type || ''}</p>
                        <button onclick="addToCart(
                            ${product.product_id}, 
                            '${product.product_name}', 
                            ${product.price})">
                            Add to Cart
                        </button>
                    `;
                    collectionGrid.appendChild(item);
                });
            })
            .catch(err => console.log('Products load error:', err));
    }

    // ─── CART ─────────────────────────────────────
    window.addToCart = function(product_id, name, price) {
        cart.push({ product_id, name, price: parseFloat(price), quantity: 1 });
        alert(`${name} added to cart!`);
        updateCartDisplay();
    };

    function updateCartDisplay() {
        const cartCount = document.getElementById('cart-count');
        if (cartCount) cartCount.innerText = cart.length;
    }

    // ─── CHECKOUT ─────────────────────────────────
    window.checkout = function() {
        if (cart.length === 0) {
            alert('Your cart is empty!');
            return;
        }

        const customer_id = localStorage.getItem('customer_id');
        if (!customer_id) {
            alert('Please login first!');
            window.location.href = 'login.html';
            return;
        }

        const totalAmount = cart.reduce((t, i) => t + i.price, 0).toFixed(2);

        const checkoutContainer = document.createElement('div');
        checkoutContainer.innerHTML = `
            <h2>Checkout</h2>
            <p>Total: Rs. ${totalAmount}</p>
            <label>Address:</label>
            <input type="text" id="address" placeholder="Your address" required>
            <label>Payment Method:</label>
            <select id="payment">
                <option value="credit-card">Credit Card</option>
                <option value="debit-card">Debit Card</option>
                <option value="paypal">PayPal</option>
            </select>
            <button onclick="confirmOrder('${totalAmount}')">Confirm Order</button>
            <button onclick="cancelCheckout()">Cancel</button>
        `;
        document.body.appendChild(checkoutContainer);
    };

    window.confirmOrder = async function(totalAmount) {
        const address = document.getElementById('address').value;
        const paymentMethod = document.getElementById('payment').value;
        const customer_id = localStorage.getItem('customer_id');

        if (!address) {
            alert('Please enter your address!');
            return;
        }

        try {
            const resp = await fetch(`${API.order}/api/orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    customer_id: parseInt(customer_id), 
                    cart: cart 
                })
            });
            const data = await resp.json();
            if (data.success) {
                alert(`Order Confirmed! Total: Rs. ${totalAmount}`);
                cart = [];
                updateCartDisplay();
                window.location.href = 'index.html';
            } else {
                alert(`Order failed: ${data.error}`);
            }
        } catch (err) {
            alert('Order service unavailable!');
        }
    };

    window.cancelCheckout = function() {
        const last = document.body.lastChild;
        if (last) document.body.removeChild(last);
    };

    // ─── LOGIN MODAL ──────────────────────────────
    window.showLoginModal = function() {
        if (!localStorage.getItem('modalDismissed')) {
            if (typeof $ !== 'undefined') {
                $('#loginModal').modal('show');
            }
        }
    };

    window.dismissModal = function() {
        if (typeof $ !== 'undefined') {
            $('#loginModal').modal('hide');
        }
        localStorage.setItem('modalDismissed', 'true');
    };

    setInterval(showLoginModal, 120000);
    showLoginModal();

    // ─── FILTER ───────────────────────────────────
    const filterButtons = document.querySelectorAll('.filter-btn');
    const productGrid = document.querySelector('.product-grid');

    if (filterButtons.length > 0 && productGrid) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.dataset.filter;
                productGrid.querySelectorAll('.product-item').forEach(item => {
                    item.style.display = 
                        (filter === 'all' || item.classList.contains(filter)) 
                        ? 'block' : 'none';
                });
            });
        });
    }

    window.updateBudgetValue = (value) => {
        const el = document.getElementById('budget-value');
        if (el) el.textContent = `Rs. ${value}`;
    };
});