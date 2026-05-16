import requests
import time
import threading

URLs = [
    "https://fashion-user-service-audqffe9dve4dscm.southeastasia-01.azurewebsites.net/api/customers",
    "https://fashion-product-service-b7atcad9dfe8g5e3.southeastasia-01.azurewebsites.net/api/products",
    "https://fashion-order-service-gxgugehgfshngyc9.southeastasia-01.azurewebsites.net/api/orders",
    "https://fashion-payment-service-hhfghcg8bya6fvd9.southeastasia-01.azurewebsites.net/api/payment/status",
]

results = []

def test_service(url):
    start = time.time()
    try:
        r = requests.get(url, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        results.append(f"✅ {url.split('/api/')[1]} → {r.status_code} — {elapsed}ms")
    except Exception as e:
        results.append(f"❌ {url} → ERROR: {e}")

# 10 concurrent users
threads = []
for i in range(10):
    for url in URLs:
        t = threading.Thread(target=test_service, args=(url,))
        threads.append(t)
        t.start()

for t in threads:
    t.join()

print("\n=== LOAD TEST RESULTS ===")
for r in results:
    print(r)
print(f"\nTotal Requests: {len(results)}")