import urllib.request
import json
import urllib.error

# Login to get token
login_req = urllib.request.Request("http://127.0.0.1:8200/api/v1/users/login", method="POST")
login_req.add_header("Content-Type", "application/x-www-form-urlencoded")
login_data = "username=prof.smith@university.edu&password=password123".encode('utf-8')

try:
    with urllib.request.urlopen(login_req, data=login_data) as response:
        login_res = json.loads(response.read().decode('utf-8'))
        token = login_res['access_token']
except urllib.error.HTTPError as e:
    print("Login Failed:", e.read().decode('utf-8'))
    exit(1)

# Generate Quiz
req = urllib.request.Request("http://127.0.0.1:8200/api/v1/modules/1/quizzes", method="POST")
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Content-Type", "application/json")
data = json.dumps({"difficulty_level": "Medium", "num_questions": 5}).encode("utf-8")

try:
    with urllib.request.urlopen(req, data=data, timeout=60) as response:
        print("Status:", response.status)
        print("Response:", response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print("Error Response:", e.read().decode("utf-8"))
except Exception as e:
    print(e)
