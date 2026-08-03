import requests
import json
import sys

def test(out):
    base_url = "http://127.0.0.1:8000/api/query"

    queries = [
        "My pan is ABCDE1234F, what is Nippon india?",
        "Which is better Nippon or SBI?",
        "What is the exit load?",
        "What is the exit load of Nippon India Small Cap Fund?"
    ]

    for q in queries:
        out.write(f"--- Query: {q} ---\n")
        try:
            res = requests.post(base_url, json={"query": q})
            out.write(str(res.json()) + "\n")
        except Exception as e:
            out.write(f"Error: {e}\n")
        out.write("\n")

if __name__ == '__main__':
    with open("test_output.txt", "w", encoding="utf-8") as out:
        test(out)
