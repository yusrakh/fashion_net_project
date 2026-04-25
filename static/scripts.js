document.addEventListener('DOMContentLoaded', function () {
    console.log('Fashion.net website loaded.');

    // Cart initialization
    let cart = []; // This should hold your cart items

    // Dynamically update the brand name on the brand.html page
    const brandNameElement = document.getElementById('brand-name');
    const categoryNameElement = document.getElementById('category-name');
    const params = new URLSearchParams(window.location.search);

    // Helper function to capitalize the first letter of any string
    const capitalizeFirstLetter = (string) => string.charAt(0).toUpperCase() + string.slice(1);

    // Helper function to format category names (capitalizes each word)
    const formatCategoryName = (string) => string.split('-').map(capitalizeFirstLetter).join(' ');

    // Update the brand name
    if (brandNameElement) {
        const brand = params.get('brand');
        brandNameElement.innerText = brand ? capitalizeFirstLetter(brand) : 'Unknown Brand';
    }

    // Update the category name
    if (categoryNameElement) {
        const category = params.get('category');
        categoryNameElement.innerText = category ? formatCategoryName(category) : 'Unknown Category';
    }

    // Example of adding a product filter based on price or category
    const productGrid = document.querySelector('.product-grid');
    const filterButtons = document.querySelectorAll('.filter-btn');

    if (filterButtons.length > 0 && productGrid) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.dataset.filter;
                const productItems = productGrid.querySelectorAll('.product-item');

                productItems.forEach(item => {
                    item.style.display = (filter === 'all' || item.classList.contains(filter)) ? 'block' : 'none';
                });
            });
        });
    }

    // Function to update budget value display
    window.updateBudgetValue = (value) => {
        document.getElementById('budget-value').textContent = `$${value}`;
    };

    // Filtering functionality
    const products = [
        { name: 'Ethnic', size: 'medium', price: 300, image: 'path/to/ethnic.jpg' },
        { name: 'Zellbury', size: 'large', price: 800, image: 'path/to/zellbury.jpg' },
        { name: 'Sapphire', size: 'small', price: 500, image: 'path/to/sapphire.jpg' },
        { name: 'Outfitters', size: 'medium', price: 200, image: 'path/to/outfitters.jpg' },
        { name: 'Saya', size: 'large', price: 600, image: 'path/to/saya.jpg' },
    ];

    function filterProducts() {
        const selectedSize = document.getElementById('size').value;
        const selectedBrand = document.getElementById('brand').value;
        const selectedBudget = parseInt(document.getElementById('budget').value);

        const filteredProducts = products.filter(product => {
            const sizeMatch = selectedSize ? product.size === selectedSize : true;
            const brandMatch = selectedBrand ? product.name.toLowerCase() === selectedBrand : true;
            const priceMatch = product.price <= selectedBudget;

            return sizeMatch && brandMatch && priceMatch;
        });

        displayProducts(filteredProducts);
    }

    function displayProducts(filteredProducts) {
        const collectionGrid = document.querySelector('.collection-grid');
        collectionGrid.innerHTML = ''; // Clear existing products

        filteredProducts.forEach(product => {
            const item = document.createElement('div');
            item.classList.add('collection-item');
            item.innerHTML = `<h3>${product.name}</h3><img src="${product.image}" alt="${product.name} Fashion">`; // Replace with actual image URL
            collectionGrid.appendChild(item);
        });
    }

    // Event listeners to filter products when any of the filters change
    document.getElementById('size').addEventListener('change', filterProducts);
    document.getElementById('brand').addEventListener('change', filterProducts);
    document.getElementById('budget').addEventListener('input', filterProducts);

    // Function to show the login modal periodically
    window.showLoginModal = function () {
        if (!localStorage.getItem('modalDismissed')) {
            $('#loginModal').modal('show');
        }
    };

    // Function to dismiss the modal
    window.dismissModal = function () {
        $('#loginModal').modal('hide'); // Dismiss the modal
        localStorage.setItem('modalDismissed', 'true'); // Set a flag in local storage
    };

    // Set an interval to show the modal every 2 minutes (120000 milliseconds)
    setInterval(showLoginModal, 120000);

    // Show modal immediately when the page loads
    showLoginModal();

    // Checkout functionality
    window.checkout = function () {
        if (cart.length === 0) {
            alert('Your cart is empty!');
            return;
        }

        const totalAmount = cart.reduce((total, item) => total + parseFloat(item.price), 0);
        const totalAmountPKR = totalAmount.toFixed(2);
        const checkoutContainer = document.createElement('div');
        
        checkoutContainer.innerHTML = `
            <h2>Checkout</h2>
            <p>Total Amount: ${totalAmountPKR} PKR</p>
            <label for="address">Enter Your Address:</label>
            <input type="text" id="address" placeholder="Your address here" required>
            <label for="payment">Enter Payment Method:</label>
            <select id="payment">
                <option value="credit-card">Credit Card</option>
                <option value="debit-card">Debit Card</option>
                <option value="paypal">PayPal</option>
            </select>
            <button onclick="confirmOrder('${totalAmountPKR}')">Confirm Order</button>
            <button onclick="cancelCheckout()">Cancel</button>
        `;

        document.body.appendChild(checkoutContainer);
    };

    window.confirmOrder = function(totalAmount) {
        const address = document.getElementById('address').value;
        const paymentMethod = document.getElementById('payment').value;

        if (!address) {
            alert("Please enter your address.");
            return;
        }

        alert(`Order Confirmed! Total Amount: ${totalAmount} PKR\nAddress: ${address}\nPayment Method: ${paymentMethod}`);
        cart = []; // Clear the cart
        displayCart(); // Update the cart display

        // Redirect to homepage or another page after checkout (optional)
        window.location.href = 'index.html'; // Change this to redirect as needed
    };

    window.cancelCheckout = function() {
        const checkoutContainer = document.body.lastChild;
        if (checkoutContainer) {
            document.body.removeChild(checkoutContainer);
        }
    };
});
