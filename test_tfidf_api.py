import requests
import json

payload = {
    "query": "What is the minimum SIP amount required to start investing?",
    "stream": False
}

try:
    r = requests.post("http://127.0.0.1:8000/api/query", json=payload)
    print("Response Status:", r.status_code)
    print("Response Content:")
    print(r.text)
except Exception as e:
    print("Request Failed:", e)
