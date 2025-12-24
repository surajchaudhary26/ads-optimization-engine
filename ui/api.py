import requests

def call_backend(payload, backend_url):
    response = requests.post(backend_url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
