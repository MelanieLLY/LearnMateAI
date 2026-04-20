import urllib.request
import json

login_req = urllib.request.Request("http://127.0.0.1:8200/api/v1/auth/token", method="POST")
login_req.add_header("Content-Type", "application/x-www-form-urlencoded")
login_data = "username=prof.smith@university.edu&password=password123".encode('utf-8')

try:
    with urllib.request.urlopen(login_req, data=login_data) as response:
        login_res = json.loads(response.read().decode('utf-8'))
        token = login_res['access_token']
except urllib.error.HTTPError as e:
    print("Login Failed:", e.read().decode('utf-8'))
    exit(1)

req = urllib.request.Request("http://127.0.0.1:8200/api/v1/modules/1/quizzes", method="GET")
req.add_header("Authorization", f"Bearer {token}")
try:
    with urllib.request.urlopen(req) as response:
        print("Quizzes:", response.status)
        data = json.loads(response.read().decode("utf-8"))
        print(f"Total quizzes found: {len(data)}")
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print("Error Response:", e.read().decode("utf-8"))
