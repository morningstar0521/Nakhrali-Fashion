#!/usr/bin/env python3
"""
Test script to verify the registration endpoint is working
"""

import requests
import json
import sys

def test_registration():
    """Test the registration endpoint"""
    
    # Backend URL
    base_url = "http://localhost:5000/api"
    
    # Test data
    test_user = {
        "first_name": "Test",
        "last_name": "User", 
        "email": "test@example.com",
        "phone": "9876543210",
        "password": "password123",
        "date_of_birth": "1990-01-01",
        "gender": "female",
        "preferred_styles": ["traditional", "modern"],
        "newsletter_subscription": True
    }
    
    print("Testing registration endpoint...")
    print(f"URL: {base_url}/auth/register")
    print(f"Data: {json.dumps(test_user, indent=2)}")
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server at http://localhost:5000")
        print("Make sure the Flask backend is running!")
        return False
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return False

def test_duplicate_registration():
    """Test registering with same email twice"""
    
    base_url = "http://localhost:5000/api"
    
    test_user = {
        "first_name": "Duplicate",
        "last_name": "User", 
        "email": "test@example.com",  # Same email as before
        "phone": "9876543211",
        "password": "password123"
    }
    
    print("\n" + "="*50)
    print("Testing duplicate email registration...")
    
    try:
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 409:
            print("✅ Duplicate email correctly rejected!")
            return True
        else:
            print("❌ Duplicate email should have been rejected!")
            return False
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Nakhrali Fashion Registration Endpoint")
    print("="*50)
    
    # Test 1: Normal registration
    success1 = test_registration()
    
    # Test 2: Duplicate email
    success2 = test_duplicate_registration()
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print(f"Normal Registration: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Duplicate Email Check: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! Registration endpoint is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the backend implementation.")
        sys.exit(1)
