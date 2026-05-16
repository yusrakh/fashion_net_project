import requests

services = {
    "User Service":    "https://fashion-user-service-audqffe9dve4dscm.southeastasia-01.azurewebsites.net/api/customers",
    "Product Service": "https://fashion-product-service-b7atcad9dfe8g5e3.southeastasia-01.azurewebsites.net/api/products",
    "Order Service":   "https://fashion-order-service-gxgugehgfshngyc9.southeastasia-01.azurewebsites.net/api/orders",
    "Payment Service": "https://fashion-payment-service-hhfghcg8bya6fvd9.southeastasia-01.azurewebsites.net/api/payment/status",
}

for name, url in services.items():
    try:
        r = requests.get(url, timeout=10)
        print(f"✅ {name}: {r.status_code}")
    except Exception as e:
        print(f"❌ {name}: DOWN — {e}")