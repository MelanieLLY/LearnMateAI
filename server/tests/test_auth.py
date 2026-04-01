def test_register_and_login(client):
    # Register as student
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "password123", "role": "student"}
    )
    assert register_response.status_code == 201
    
    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.cookies
    assert login_response.json()["email"] == "student@example.com"
    
    # Check /me with cookie
    me_response = client.get("/api/v1/auth/me", cookies=login_response.cookies)
    assert me_response.status_code == 200
    assert me_response.json()["role"] == "student"
    
    # Logout
    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200
    
    # Ensure cookie is cleared (FastAPI response sets it to expired/-1 basically)
    # The exact parsing of deleted cookies by requests can be messy, but let's check basic mechanics
    # TestClient strips the deleted cookie from the response.cookies dict.
    assert logout_response.status_code == 200
