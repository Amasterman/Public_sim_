import requests

r = requests.get("http://127.0.0.1:5000/tile/v1/driving/tile(50.91985,1.3568,20)")

res = r.json()