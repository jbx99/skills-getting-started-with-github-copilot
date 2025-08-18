"""
Unit tests for the authentication functionality.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Add the src directory to the path so we can import the app module
sys.path.append(str(Path(__file__).parent.parent))
from src.app import app, User

# Create a test client
client = TestClient(app)

class TestAuthentication:
    """Test class for authentication endpoints"""
    
    def test_login_successful(self):
        """Test successful login returns a token"""
        response = client.post(
            "/token",
            json={"username": "testuser", "password": "password"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self):
        """Test login with wrong password returns 401"""
        response = client.post(
            "/token",
            json={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        
    def test_get_user_info_with_token(self):
        """Test getting user info with valid token"""
        # First get a token
        login_response = client.post(
            "/token",
            json={"username": "testuser", "password": "password"}
        )
        token = login_response.json()["access_token"]
        
        # Then use token to get user info
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "testuser@mergington.edu"
        
    def test_get_user_info_without_token(self):
        """Test accessing protected endpoint without token returns 401"""
        response = client.get("/users/me")
        assert response.status_code == 401
        
    def test_get_user_info_invalid_token(self):
        """Test accessing protected endpoint with invalid token returns 401"""
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalidtoken"}
        )
        assert response.status_code == 401
