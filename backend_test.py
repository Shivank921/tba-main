#!/usr/bin/env python3
"""
Backend API Testing for Bengali Association Coimbatore
Tests the contact form and newsletter subscription endpoints
"""

import requests
import json
from datetime import datetime

# Base URL from frontend/.env
BASE_URL = "https://prep-changes-1.preview.emergentagent.com/api"

def print_test_header(test_name):
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")

def print_result(passed, message):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")

def test_contact_valid_with_all_fields():
    """Test POST /api/contact with all fields including optional phone"""
    print_test_header("Contact Form - Valid submission with all fields")
    
    payload = {
        "name": "Rajesh Kumar",
        "email": "rajesh.kumar@example.com",
        "phone": "+919876543210",
        "message": "Hello, I am interested in becoming a member of the Bengali Association."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            # Verify all required fields are present
            checks = [
                ('id' in data, "Response has 'id' field"),
                ('name' in data and data['name'] == payload['name'], "Name matches"),
                ('email' in data and data['email'] == payload['email'], "Email matches"),
                ('phone' in data and data['phone'] == payload['phone'], "Phone matches"),
                ('message' in data and data['message'] == payload['message'], "Message matches"),
                ('created_at' in data, "Has 'created_at' timestamp"),
                ('_id' not in data, "MongoDB _id not exposed")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Verify created_at is valid ISO datetime
            try:
                datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                print_result(True, "created_at is valid ISO datetime")
            except:
                print_result(False, "created_at is NOT valid ISO datetime")
                all_passed = False
            
            return all_passed
        else:
            print_result(False, f"Expected 201, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_without_phone():
    """Test POST /api/contact without optional phone field"""
    print_test_header("Contact Form - Valid submission without phone (optional)")
    
    payload = {
        "name": "Ananya Chatterjee",
        "email": "ananya.c@example.com",
        "message": "I would like to know more about upcoming cultural events."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            checks = [
                ('id' in data, "Response has 'id' field"),
                ('name' in data, "Has name field"),
                ('email' in data, "Has email field"),
                ('message' in data, "Has message field"),
                ('created_at' in data, "Has created_at field"),
                (data.get('phone') is None, "Phone is None (not required)")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            return all_passed
        else:
            print_result(False, f"Expected 201, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_missing_name():
    """Test POST /api/contact with missing name field"""
    print_test_header("Contact Form - Missing required 'name' field")
    
    payload = {
        "email": "test@example.com",
        "message": "This should fail due to missing name"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for missing name, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_invalid_email():
    """Test POST /api/contact with invalid email format"""
    print_test_header("Contact Form - Invalid email format")
    
    payload = {
        "name": "Test User",
        "email": "not-a-valid-email",
        "message": "This should fail due to invalid email"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for invalid email, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_empty_message():
    """Test POST /api/contact with empty message"""
    print_test_header("Contact Form - Empty message field")
    
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "message": ""
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for empty message, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_get_list_protected():
    """Test GET /api/contact now requires authentication"""
    print_test_header("Contact Form - GET list requires auth (protected)")
    
    try:
        # Test without token - should return 401
        response = requests.get(f"{BASE_URL}/contact", timeout=10)
        print(f"Status Code (no auth): {response.status_code}")
        
        if response.status_code == 401:
            print_result(True, "GET /api/contact correctly returns 401 without auth")
            return True
        else:
            print_result(False, f"Expected 401 without auth, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_get_list_with_auth(token):
    """Test GET /api/contact with valid token"""
    print_test_header("Contact Form - GET list with valid token")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/contact", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of contacts: {len(data)}")
            
            if len(data) > 0:
                print(f"Sample (most recent): {json.dumps(data[0], indent=2)}")
                
                # Verify structure
                first = data[0]
                checks = [
                    ('id' in first, "Has 'id' field"),
                    ('name' in first, "Has 'name' field"),
                    ('email' in first, "Has 'email' field"),
                    ('message' in first, "Has 'message' field"),
                    ('created_at' in first, "Has 'created_at' field"),
                    ('handled' in first, "Has 'handled' field"),
                    ('_id' not in first, "MongoDB _id not exposed")
                ]
                
                all_passed = True
                for check, desc in checks:
                    print_result(check, desc)
                    if not check:
                        all_passed = False
                
                # Check if sorted by most recent first
                if len(data) >= 2:
                    first_time = datetime.fromisoformat(data[0]['created_at'].replace('Z', '+00:00'))
                    second_time = datetime.fromisoformat(data[1]['created_at'].replace('Z', '+00:00'))
                    sorted_check = first_time >= second_time
                    print_result(sorted_check, "Results sorted by most recent first")
                    if not sorted_check:
                        all_passed = False
                
                return all_passed
            else:
                print_result(True, "GET endpoint works with auth (empty list)")
                return True
        else:
            print_result(False, f"Expected 200 with auth, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_valid():
    """Test POST /api/newsletter with valid email"""
    print_test_header("Newsletter - Valid subscription")
    
    # Use a unique email for this test
    test_email = f"subscriber.{datetime.now().timestamp()}@example.com"
    payload = {"email": test_email}
    
    try:
        response = requests.post(f"{BASE_URL}/newsletter", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            checks = [
                ('id' in data, "Response has 'id' field"),
                ('email' in data, "Has 'email' field"),
                ('subscribed_at' in data, "Has 'subscribed_at' timestamp"),
                ('_id' not in data, "MongoDB _id not exposed"),
                (data['email'] == test_email.lower(), "Email is lowercased")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Store the ID for idempotency test
            global first_subscription_id
            first_subscription_id = data['id']
            
            return all_passed
        else:
            print_result(False, f"Expected 201, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_idempotent():
    """Test POST /api/newsletter idempotency - same email twice"""
    print_test_header("Newsletter - Idempotency check (duplicate email)")
    
    # Use a specific email for idempotency test
    test_email = "idempotency.test@example.com"
    payload = {"email": test_email}
    
    try:
        # First submission
        print("First submission:")
        response1 = requests.post(f"{BASE_URL}/newsletter", json=payload, timeout=10)
        print(f"Status Code: {response1.status_code}")
        print(f"Response: {json.dumps(response1.json(), indent=2)}")
        
        if response1.status_code != 201:
            print_result(False, f"First submission failed with {response1.status_code}")
            return False
        
        data1 = response1.json()
        id1 = data1['id']
        
        # Second submission (duplicate)
        print("\nSecond submission (duplicate):")
        response2 = requests.post(f"{BASE_URL}/newsletter", json=payload, timeout=10)
        print(f"Status Code: {response2.status_code}")
        print(f"Response: {json.dumps(response2.json(), indent=2)}")
        
        if response2.status_code != 201:
            print_result(False, f"Second submission failed with {response2.status_code}")
            return False
        
        data2 = response2.json()
        id2 = data2['id']
        
        # Verify idempotency
        checks = [
            (id1 == id2, f"Same ID returned (id1={id1}, id2={id2})"),
            (data1['email'] == data2['email'], "Same email returned"),
            (data1['subscribed_at'] == data2['subscribed_at'], "Same subscribed_at timestamp")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(check, desc)
            if not check:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_invalid_email():
    """Test POST /api/newsletter with invalid email"""
    print_test_header("Newsletter - Invalid email format")
    
    payload = {"email": "not-valid-email"}
    
    try:
        response = requests.post(f"{BASE_URL}/newsletter", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for invalid email, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_missing_email():
    """Test POST /api/newsletter with missing email"""
    print_test_header("Newsletter - Missing email field")
    
    payload = {}
    
    try:
        response = requests.post(f"{BASE_URL}/newsletter", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for missing email, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_get_list_protected():
    """Test GET /api/newsletter now requires authentication"""
    print_test_header("Newsletter - GET list requires auth (protected)")
    
    try:
        # Test without token - should return 401
        response = requests.get(f"{BASE_URL}/newsletter", timeout=10)
        print(f"Status Code (no auth): {response.status_code}")
        
        if response.status_code == 401:
            print_result(True, "GET /api/newsletter correctly returns 401 without auth")
            return True
        else:
            print_result(False, f"Expected 401 without auth, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_newsletter_get_list_with_auth(token):
    """Test GET /api/newsletter with valid token"""
    print_test_header("Newsletter - GET list with valid token")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/newsletter", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of subscribers: {len(data)}")
            
            if len(data) > 0:
                print(f"Sample (most recent): {json.dumps(data[0], indent=2)}")
                
                # Verify structure
                first = data[0]
                checks = [
                    ('id' in first, "Has 'id' field"),
                    ('email' in first, "Has 'email' field"),
                    ('subscribed_at' in first, "Has 'subscribed_at' field"),
                    ('_id' not in first, "MongoDB _id not exposed")
                ]
                
                all_passed = True
                for check, desc in checks:
                    print_result(check, desc)
                    if not check:
                        all_passed = False
                
                return all_passed
            else:
                print_result(True, "GET endpoint works with auth (empty list)")
                return True
        else:
            print_result(False, f"Expected 200 with auth, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

# ============================================================
# Admin Auth Tests
# ============================================================

def test_admin_login_valid():
    """Test POST /api/admin/login with valid credentials"""
    print_test_header("Admin Login - Valid credentials")
    
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('access_token' in data, "Response has 'access_token' field"),
                ('token_type' in data and data['token_type'] == 'bearer', "token_type is 'bearer'"),
                ('username' in data and data['username'] == 'admin', "username is 'admin'"),
                ('expires_hours' in data, "Has 'expires_hours' field")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Return token for use in other tests
            return all_passed, data.get('access_token', '')
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False, ''
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, ''

def test_admin_login_wrong_password():
    """Test POST /api/admin/login with wrong password"""
    print_test_header("Admin Login - Wrong password")
    
    payload = {
        "username": "admin",
        "password": "WrongPassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            data = response.json()
            has_detail = 'detail' in data
            print_result(has_detail, "Response has 'detail' field with error message")
            print_result(True, "Correctly returns 401 for wrong password")
            return True
        else:
            print_result(False, f"Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_login_unknown_username():
    """Test POST /api/admin/login with unknown username"""
    print_test_header("Admin Login - Unknown username")
    
    payload = {
        "username": "nonexistent_user",
        "password": "SomePassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 401
        print_result(passed, f"Expected 401 for unknown username, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_login_missing_fields():
    """Test POST /api/admin/login with missing fields"""
    print_test_header("Admin Login - Missing fields")
    
    # Test missing password
    payload = {"username": "admin"}
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code (missing password): {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 422
        print_result(passed, f"Expected 422 for missing password, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_me_without_token():
    """Test GET /api/admin/me without Authorization header"""
    print_test_header("Admin Me - Without Authorization header")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/me", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 401
        print_result(passed, f"Expected 401 without token, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_me_invalid_token():
    """Test GET /api/admin/me with invalid token"""
    print_test_header("Admin Me - Invalid token")
    
    try:
        headers = {"Authorization": "Bearer invalid_token_12345"}
        response = requests.get(f"{BASE_URL}/admin/me", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 401
        print_result(passed, f"Expected 401 for invalid token, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_me_valid_token(token):
    """Test GET /api/admin/me with valid token"""
    print_test_header("Admin Me - Valid token")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/admin/me", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('username' in data and data['username'] == 'admin', "username is 'admin'"),
                ('role' in data and data['role'] == 'admin', "role is 'admin'")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_stats_without_token():
    """Test GET /api/admin/stats without token"""
    print_test_header("Admin Stats - Without token")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/stats", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        passed = response.status_code == 401
        print_result(passed, f"Expected 401 without token, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_admin_stats_valid_token(token):
    """Test GET /api/admin/stats with valid token"""
    print_test_header("Admin Stats - Valid token")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/admin/stats", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('total_inquiries' in data and isinstance(data['total_inquiries'], int), "Has 'total_inquiries' (int)"),
                ('pending_inquiries' in data and isinstance(data['pending_inquiries'], int), "Has 'pending_inquiries' (int)"),
                ('handled_inquiries' in data and isinstance(data['handled_inquiries'], int), "Has 'handled_inquiries' (int)"),
                ('total_subscribers' in data and isinstance(data['total_subscribers'], int), "Has 'total_subscribers' (int)")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_patch_without_token():
    """Test PATCH /api/contact/{id} without token"""
    print_test_header("Contact Patch - Without token")
    
    # First create a contact to get an ID
    contact_payload = {
        "name": "Patch Test User",
        "email": "patchtest@example.com",
        "message": "This is a test contact for patch testing"
    }
    
    try:
        # Create contact
        create_response = requests.post(f"{BASE_URL}/contact", json=contact_payload, timeout=10)
        if create_response.status_code != 201:
            print_result(False, f"Failed to create test contact: {create_response.status_code}")
            return False, None
        
        contact_id = create_response.json()['id']
        print(f"Created test contact with ID: {contact_id}")
        
        # Try to patch without token
        patch_payload = {"handled": True}
        response = requests.patch(f"{BASE_URL}/contact/{contact_id}", json=patch_payload, timeout=10)
        print(f"Status Code (no auth): {response.status_code}")
        
        passed = response.status_code == 401
        print_result(passed, f"Expected 401 without token, got {response.status_code}")
        return passed, contact_id
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_contact_patch_with_token(token, contact_id):
    """Test PATCH /api/contact/{id} with valid token"""
    print_test_header("Contact Patch - Mark handled=true with token")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Mark as handled
        patch_payload = {"handled": True}
        response = requests.patch(f"{BASE_URL}/contact/{contact_id}", json=patch_payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            check1 = data.get('handled') == True
            print_result(check1, f"handled field is True: {data.get('handled')}")
            
            # Now mark as not handled
            print("\nMarking as handled=false:")
            patch_payload2 = {"handled": False}
            response2 = requests.patch(f"{BASE_URL}/contact/{contact_id}", json=patch_payload2, headers=headers, timeout=10)
            print(f"Status Code: {response2.status_code}")
            print(f"Response: {json.dumps(response2.json(), indent=2)}")
            
            if response2.status_code == 200:
                data2 = response2.json()
                check2 = data2.get('handled') == False
                print_result(check2, f"handled field is False: {data2.get('handled')}")
                return check1 and check2
            else:
                print_result(False, f"Expected 200 for second patch, got {response2.status_code}")
                return False
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_contact_patch_nonexistent_id(token):
    """Test PATCH /api/contact/{id} with non-existent ID"""
    print_test_header("Contact Patch - Non-existent ID")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        fake_id = "nonexistent-id-12345"
        patch_payload = {"handled": True}
        
        response = requests.patch(f"{BASE_URL}/contact/{fake_id}", json=patch_payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 404
        print_result(passed, f"Expected 404 for non-existent ID, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_stats_after_marking_handled(token):
    """Test that stats update correctly after marking contact as handled"""
    print_test_header("Admin Stats - Verify counts after marking handled")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get initial stats
        response1 = requests.get(f"{BASE_URL}/admin/stats", headers=headers, timeout=10)
        if response1.status_code != 200:
            print_result(False, f"Failed to get initial stats: {response1.status_code}")
            return False
        
        stats1 = response1.json()
        print(f"Initial stats: {json.dumps(stats1, indent=2)}")
        
        # Create a new contact
        contact_payload = {
            "name": "Stats Test User",
            "email": "statstest@example.com",
            "message": "Testing stats update"
        }
        create_response = requests.post(f"{BASE_URL}/contact", json=contact_payload, timeout=10)
        if create_response.status_code != 201:
            print_result(False, f"Failed to create test contact: {create_response.status_code}")
            return False
        
        contact_id = create_response.json()['id']
        
        # Get stats after creating contact
        response2 = requests.get(f"{BASE_URL}/admin/stats", headers=headers, timeout=10)
        stats2 = response2.json()
        print(f"Stats after creating contact: {json.dumps(stats2, indent=2)}")
        
        # Mark contact as handled
        patch_payload = {"handled": True}
        patch_response = requests.patch(f"{BASE_URL}/contact/{contact_id}", json=patch_payload, headers=headers, timeout=10)
        if patch_response.status_code != 200:
            print_result(False, f"Failed to mark contact as handled: {patch_response.status_code}")
            return False
        
        # Get stats after marking handled
        response3 = requests.get(f"{BASE_URL}/admin/stats", headers=headers, timeout=10)
        stats3 = response3.json()
        print(f"Stats after marking handled: {json.dumps(stats3, indent=2)}")
        
        # Verify stats changed correctly
        checks = [
            (stats2['total_inquiries'] == stats1['total_inquiries'] + 1, 
             f"Total inquiries increased by 1: {stats1['total_inquiries']} -> {stats2['total_inquiries']}"),
            (stats2['pending_inquiries'] == stats1['pending_inquiries'] + 1,
             f"Pending inquiries increased by 1: {stats1['pending_inquiries']} -> {stats2['pending_inquiries']}"),
            (stats3['pending_inquiries'] == stats2['pending_inquiries'] - 1,
             f"Pending inquiries decreased by 1 after marking handled: {stats2['pending_inquiries']} -> {stats3['pending_inquiries']}"),
            (stats3['handled_inquiries'] == stats2['handled_inquiries'] + 1,
             f"Handled inquiries increased by 1: {stats2['handled_inquiries']} -> {stats3['handled_inquiries']}")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(check, desc)
            if not check:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

# ============================================================
# Gallery Management Tests
# ============================================================

def test_gallery_get_public():
    """Test GET /api/gallery - Public endpoint returning all albums"""
    print_test_header("Gallery - GET /api/gallery (PUBLIC)")
    
    try:
        response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            albums = response.json()
            print(f"Number of albums: {len(albums)}")
            print(f"Response: {json.dumps(albums, indent=2)}")
            
            checks = [
                (len(albums) == 4, f"Expected 4 albums, got {len(albums)}"),
                (albums[0]['id'] == 'puja', f"First album is 'puja', got '{albums[0]['id']}'"),
                (albums[1]['id'] == 'programs', f"Second album is 'programs', got '{albums[1]['id']}'"),
                (albums[2]['id'] == 'activities', f"Third album is 'activities', got '{albums[2]['id']}'"),
                (albums[3]['id'] == 'news-media', f"Fourth album is 'news-media', got '{albums[3]['id']}'"),
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Check structure of first album
            if len(albums) > 0:
                album = albums[0]
                structure_checks = [
                    ('id' in album, "Album has 'id' field"),
                    ('title' in album, "Album has 'title' field"),
                    ('blurb' in album, "Album has 'blurb' field"),
                    ('cover' in album, "Album has 'cover' field"),
                    ('cover_photo_id' in album, "Album has 'cover_photo_id' field"),
                    ('photos' in album, "Album has 'photos' field"),
                    (isinstance(album['photos'], list), "Photos is a list"),
                    (len(album['photos']) == 5, f"Album has 5 photos, got {len(album['photos'])}"),
                    ('_id' not in album, "MongoDB _id not exposed")
                ]
                
                for check, desc in structure_checks:
                    print_result(check, desc)
                    if not check:
                        all_passed = False
                
                # Check photo structure
                if len(album['photos']) > 0:
                    photo = album['photos'][0]
                    photo_checks = [
                        ('id' in photo, "Photo has 'id' field"),
                        ('url' in photo, "Photo has 'url' field"),
                        ('file' in photo, "Photo has 'file' field"),
                        ('created_at' in photo, "Photo has 'created_at' field")
                    ]
                    
                    for check, desc in photo_checks:
                        print_result(check, desc)
                        if not check:
                            all_passed = False
            
            return all_passed, albums
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False, None
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None


def test_gallery_upload_without_auth():
    """Test POST /api/gallery/albums/puja/photos without JWT returns 401/403"""
    print_test_header("Gallery Upload - Without JWT (should return 401/403)")
    
    try:
        # Create a small test image (1x1 PNG)
        import io
        from PIL import Image
        
        img = Image.new('RGB', (1, 1), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/gallery/albums/puja/photos", files=files, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        passed = response.status_code in [401, 403]
        print_result(passed, f"Expected 401 or 403 without auth, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_upload_with_auth(token):
    """Test POST /api/gallery/albums/puja/photos with JWT and valid image"""
    print_test_header("Gallery Upload - With JWT and valid image")
    
    try:
        # Create a small test image (10x10 PNG)
        import io
        from PIL import Image
        
        img = Image.new('RGB', (10, 10), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        headers = {"Authorization": f"Bearer {token}"}
        files = {'file': ('test_upload.png', img_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/gallery/albums/puja/photos", files=files, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            photo = response.json()
            checks = [
                ('id' in photo, "Photo has 'id' field"),
                ('url' in photo, "Photo has 'url' field"),
                ('file' in photo, "Photo has 'file' field"),
                ('created_at' in photo, "Photo has 'created_at' field"),
                (photo['url'].startswith('/api/uploads/'), f"URL starts with '/api/uploads/', got '{photo['url']}'")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            return all_passed, photo
        else:
            print_result(False, f"Expected 201, got {response.status_code}")
            return False, None
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None


def test_gallery_serve_uploaded_file(photo_url):
    """Test GET /api/uploads/{filename} serves the uploaded file"""
    print_test_header("Gallery - Serve uploaded file via GET /api/uploads/{filename}")
    
    try:
        # Extract filename from photo URL
        filename = photo_url.split('/')[-1]
        response = requests.get(f"{BASE_URL}/uploads/{filename}", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        checks = [
            (response.status_code == 200, f"Expected 200, got {response.status_code}"),
            (len(response.content) > 0, f"File has content ({len(response.content)} bytes)")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(check, desc)
            if not check:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_upload_non_image(token):
    """Test POST /api/gallery/albums/puja/photos with non-image file returns 400"""
    print_test_header("Gallery Upload - Non-image file (should return 400)")
    
    try:
        import io
        
        # Create a text file
        text_content = io.BytesIO(b"This is a text file, not an image")
        
        headers = {"Authorization": f"Bearer {token}"}
        files = {'file': ('test.txt', text_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/gallery/albums/puja/photos", files=files, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 400
        print_result(passed, f"Expected 400 for non-image file, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_upload_large_file(token):
    """Test POST /api/gallery/albums/puja/photos with file > 15MB returns 400"""
    print_test_header("Gallery Upload - File larger than 15MB (should return 400)")
    
    try:
        import io
        
        # Create a file larger than 15MB (15 * 1024 * 1024 + 1 bytes)
        large_content = io.BytesIO(b"x" * (15 * 1024 * 1024 + 1))
        
        headers = {"Authorization": f"Bearer {token}"}
        files = {'file': ('large.png', large_content, 'image/png')}
        response = requests.post(f"{BASE_URL}/gallery/albums/puja/photos", files=files, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        passed = response.status_code == 400
        print_result(passed, f"Expected 400 for file > 15MB, got {response.status_code}")
        return passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_set_cover(token, photo_id):
    """Test PATCH /api/gallery/albums/puja/cover with JWT"""
    print_test_header("Gallery - Set cover photo with PATCH")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"photo_id": photo_id}
        response = requests.patch(f"{BASE_URL}/gallery/albums/puja/cover", json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('ok' in data and data['ok'] == True, "Response has 'ok': true"),
                ('cover' in data, "Response has 'cover' field")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Verify cover is set in GET /api/gallery
            gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
            if gallery_response.status_code == 200:
                albums = gallery_response.json()
                puja_album = next((a for a in albums if a['id'] == 'puja'), None)
                if puja_album:
                    cover_check = puja_album.get('cover') == data.get('cover')
                    cover_photo_id_check = puja_album.get('cover_photo_id') == photo_id
                    print_result(cover_check, f"Cover updated in GET /api/gallery: {puja_album.get('cover')}")
                    print_result(cover_photo_id_check, f"cover_photo_id set to {photo_id}")
                    all_passed = all_passed and cover_check and cover_photo_id_check
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_reorder_photos(token, photo_id):
    """Test PUT /api/gallery/albums/puja/order with JWT"""
    print_test_header("Gallery - Reorder photos with PUT")
    
    try:
        # Get current photos
        gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        if gallery_response.status_code != 200:
            print_result(False, "Failed to get current gallery state")
            return False
        
        albums = gallery_response.json()
        puja_album = next((a for a in albums if a['id'] == 'puja'), None)
        if not puja_album:
            print_result(False, "Puja album not found")
            return False
        
        current_photos = puja_album['photos']
        print(f"Current photo count: {len(current_photos)}")
        
        # Create new order with uploaded photo first
        photo_ids = [photo_id] + [p['id'] for p in current_photos if p['id'] != photo_id]
        print(f"New order (uploaded photo first): {photo_ids[:3]}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"photo_ids": photo_ids}
        response = requests.put(f"{BASE_URL}/gallery/albums/puja/order", json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('ok' in data and data['ok'] == True, "Response has 'ok': true"),
                ('count' in data, "Response has 'count' field")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Verify order in GET /api/gallery
            gallery_response2 = requests.get(f"{BASE_URL}/gallery", timeout=10)
            if gallery_response2.status_code == 200:
                albums2 = gallery_response2.json()
                puja_album2 = next((a for a in albums2 if a['id'] == 'puja'), None)
                if puja_album2:
                    new_photos = puja_album2['photos']
                    first_photo_check = new_photos[0]['id'] == photo_id
                    print_result(first_photo_check, f"First photo is now the uploaded photo: {new_photos[0]['id']}")
                    all_passed = all_passed and first_photo_check
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_reorder_partial_list(token):
    """Test PUT /api/gallery/albums/puja/order with partial photo_ids list"""
    print_test_header("Gallery - Reorder with partial list (missing IDs appended)")
    
    try:
        # Get current photos
        gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        if gallery_response.status_code != 200:
            print_result(False, "Failed to get current gallery state")
            return False
        
        albums = gallery_response.json()
        puja_album = next((a for a in albums if a['id'] == 'puja'), None)
        if not puja_album:
            print_result(False, "Puja album not found")
            return False
        
        current_photos = puja_album['photos']
        total_count = len(current_photos)
        print(f"Total photos: {total_count}")
        
        # Send only first 2 photo IDs
        partial_ids = [p['id'] for p in current_photos[:2]]
        print(f"Sending partial list with {len(partial_ids)} IDs")
        
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"photo_ids": partial_ids}
        response = requests.put(f"{BASE_URL}/gallery/albums/puja/order", json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Verify all photos still present
            gallery_response2 = requests.get(f"{BASE_URL}/gallery", timeout=10)
            if gallery_response2.status_code == 200:
                albums2 = gallery_response2.json()
                puja_album2 = next((a for a in albums2 if a['id'] == 'puja'), None)
                if puja_album2:
                    new_count = len(puja_album2['photos'])
                    check = new_count == total_count
                    print_result(check, f"All photos preserved: {new_count}/{total_count}")
                    return check
            
            return False
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_delete_photo(token, photo_id, photo_url):
    """Test DELETE /api/gallery/albums/puja/photos/{photo_id} with JWT"""
    print_test_header("Gallery - Delete photo with DELETE")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{BASE_URL}/gallery/albums/puja/photos/{photo_id}", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('ok' in data and data['ok'] == True, "Response has 'ok': true"),
                ('deleted' in data and data['deleted'] == photo_id, f"Deleted photo ID matches: {photo_id}")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Verify photo removed from GET /api/gallery
            gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
            if gallery_response.status_code == 200:
                albums = gallery_response.json()
                puja_album = next((a for a in albums if a['id'] == 'puja'), None)
                if puja_album:
                    photo_ids = [p['id'] for p in puja_album['photos']]
                    removed_check = photo_id not in photo_ids
                    print_result(removed_check, f"Photo removed from album (not in {len(photo_ids)} photos)")
                    all_passed = all_passed and removed_check
            
            # Verify file deleted (GET /api/uploads/{filename} returns 404)
            filename = photo_url.split('/')[-1]
            file_response = requests.get(f"{BASE_URL}/uploads/{filename}", timeout=10)
            file_deleted_check = file_response.status_code == 404
            print_result(file_deleted_check, f"Uploaded file deleted (GET returns {file_response.status_code})")
            all_passed = all_passed and file_deleted_check
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_cover_fallback_after_delete(token):
    """Test that cover falls back to first photo after deleting cover photo"""
    print_test_header("Gallery - Cover fallback after deleting cover photo")
    
    try:
        # Get current state
        gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        if gallery_response.status_code != 200:
            print_result(False, "Failed to get current gallery state")
            return False
        
        albums = gallery_response.json()
        puja_album = next((a for a in albums if a['id'] == 'puja'), None)
        if not puja_album:
            print_result(False, "Puja album not found")
            return False
        
        original_cover = puja_album.get('cover')
        print(f"Current cover: {original_cover}")
        
        # The cover should have fallen back to first remaining photo after previous delete
        # Verify cover is set to a valid photo
        if puja_album['photos']:
            first_photo_url = puja_album['photos'][0]['url']
            cover_check = puja_album.get('cover') == first_photo_url
            print_result(cover_check, f"Cover is first photo: {puja_album.get('cover')}")
            return cover_check
        else:
            print_result(False, "No photos in album")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_invalid_album_id(token):
    """Test operations with invalid album ID return 404"""
    print_test_header("Gallery - Invalid album ID returns 404")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test upload to invalid album
        import io
        from PIL import Image
        
        img = Image.new('RGB', (1, 1), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        response1 = requests.post(f"{BASE_URL}/gallery/albums/invalid-album/photos", files=files, headers=headers, timeout=10)
        print(f"Upload to invalid album - Status: {response1.status_code}")
        check1 = response1.status_code == 404
        print_result(check1, f"Upload returns 404 for invalid album")
        
        # Test delete from invalid album
        response2 = requests.delete(f"{BASE_URL}/gallery/albums/invalid-album/photos/some-id", headers=headers, timeout=10)
        print(f"Delete from invalid album - Status: {response2.status_code}")
        check2 = response2.status_code == 404
        print_result(check2, f"Delete returns 404 for invalid album")
        
        # Test reorder invalid album
        payload = {"photo_ids": ["id1", "id2"]}
        response3 = requests.put(f"{BASE_URL}/gallery/albums/invalid-album/order", json=payload, headers=headers, timeout=10)
        print(f"Reorder invalid album - Status: {response3.status_code}")
        check3 = response3.status_code == 404
        print_result(check3, f"Reorder returns 404 for invalid album")
        
        # Test set cover on invalid album
        payload2 = {"photo_id": "some-id"}
        response4 = requests.patch(f"{BASE_URL}/gallery/albums/invalid-album/cover", json=payload2, headers=headers, timeout=10)
        print(f"Set cover on invalid album - Status: {response4.status_code}")
        check4 = response4.status_code == 404
        print_result(check4, f"Set cover returns 404 for invalid album")
        
        return check1 and check2 and check3 and check4
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_invalid_photo_id(token):
    """Test operations with invalid photo ID return 404"""
    print_test_header("Gallery - Invalid photo ID returns 404")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test delete invalid photo
        response1 = requests.delete(f"{BASE_URL}/gallery/albums/puja/photos/invalid-photo-id", headers=headers, timeout=10)
        print(f"Delete invalid photo - Status: {response1.status_code}")
        check1 = response1.status_code == 404
        print_result(check1, f"Delete returns 404 for invalid photo ID")
        
        # Test set cover with invalid photo ID
        payload = {"photo_id": "invalid-photo-id"}
        response2 = requests.patch(f"{BASE_URL}/gallery/albums/puja/cover", json=payload, headers=headers, timeout=10)
        print(f"Set cover with invalid photo - Status: {response2.status_code}")
        check2 = response2.status_code == 404
        print_result(check2, f"Set cover returns 404 for invalid photo ID")
        
        return check1 and check2
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_gallery_cleanup_restore_original(token):
    """Clean up test photos and restore puja album to original 5 seeded photos"""
    print_test_header("Gallery - Cleanup and restore original state")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get current state
        gallery_response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        if gallery_response.status_code != 200:
            print_result(False, "Failed to get current gallery state")
            return False
        
        albums = gallery_response.json()
        puja_album = next((a for a in albums if a['id'] == 'puja'), None)
        if not puja_album:
            print_result(False, "Puja album not found")
            return False
        
        print(f"Current photo count: {len(puja_album['photos'])}")
        
        # Delete any uploaded photos (those with file field set and starting with /api/uploads/)
        deleted_count = 0
        for photo in puja_album['photos']:
            if photo.get('file') and photo['url'].startswith('/api/uploads/'):
                print(f"Deleting uploaded photo: {photo['id']}")
                response = requests.delete(f"{BASE_URL}/gallery/albums/puja/photos/{photo['id']}", headers=headers, timeout=10)
                if response.status_code == 200:
                    deleted_count += 1
        
        print(f"Deleted {deleted_count} uploaded test photos")
        
        # Verify final state
        gallery_response2 = requests.get(f"{BASE_URL}/gallery", timeout=10)
        if gallery_response2.status_code == 200:
            albums2 = gallery_response2.json()
            puja_album2 = next((a for a in albums2 if a['id'] == 'puja'), None)
            if puja_album2:
                final_count = len(puja_album2['photos'])
                cover = puja_album2.get('cover')
                
                checks = [
                    (final_count == 5, f"Puja album has 5 photos: {final_count}"),
                    (cover == '/durga-puja-dhunuchi.webp', f"Cover restored to '/durga-puja-dhunuchi.webp': {cover}")
                ]
                
                all_passed = True
                for check, desc in checks:
                    print_result(check, desc)
                    if not check:
                        all_passed = False
                
                return all_passed
        
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def main():
    print("\n" + "="*80)
    print("BACKEND API TESTING - Bengali Association Coimbatore")
    print(f"Base URL: {BASE_URL}")
    print("="*80)
    
    results = {}
    admin_token = None
    test_contact_id = None
    uploaded_photo = None
    uploaded_photo_id = None
    uploaded_photo_url = None
    
    # Admin Auth Tests
    print("\n\n" + "#"*80)
    print("# ADMIN AUTH ENDPOINT TESTS")
    print("#"*80)
    
    # Login tests
    login_passed, admin_token = test_admin_login_valid()
    results['admin_login_valid'] = login_passed
    results['admin_login_wrong_password'] = test_admin_login_wrong_password()
    results['admin_login_unknown_username'] = test_admin_login_unknown_username()
    results['admin_login_missing_fields'] = test_admin_login_missing_fields()
    
    # Admin /me tests
    results['admin_me_without_token'] = test_admin_me_without_token()
    results['admin_me_invalid_token'] = test_admin_me_invalid_token()
    if admin_token:
        results['admin_me_valid_token'] = test_admin_me_valid_token(admin_token)
    else:
        print_result(False, "Skipping admin_me_valid_token - no token available")
        results['admin_me_valid_token'] = False
    
    # Admin stats tests
    results['admin_stats_without_token'] = test_admin_stats_without_token()
    if admin_token:
        results['admin_stats_valid_token'] = test_admin_stats_valid_token(admin_token)
    else:
        print_result(False, "Skipping admin_stats_valid_token - no token available")
        results['admin_stats_valid_token'] = False
    
    # Contact Form Tests (Public POST)
    print("\n\n" + "#"*80)
    print("# CONTACT FORM ENDPOINT TESTS (Public POST)")
    print("#"*80)
    
    results['contact_valid_all_fields'] = test_contact_valid_with_all_fields()
    results['contact_without_phone'] = test_contact_without_phone()
    results['contact_missing_name'] = test_contact_missing_name()
    results['contact_invalid_email'] = test_contact_invalid_email()
    results['contact_empty_message'] = test_contact_empty_message()
    
    # Contact GET (now protected)
    print("\n\n" + "#"*80)
    print("# CONTACT GET ENDPOINT TESTS (Protected)")
    print("#"*80)
    
    results['contact_get_list_protected'] = test_contact_get_list_protected()
    if admin_token:
        results['contact_get_list_with_auth'] = test_contact_get_list_with_auth(admin_token)
    else:
        print_result(False, "Skipping contact_get_list_with_auth - no token available")
        results['contact_get_list_with_auth'] = False
    
    # Contact PATCH tests
    print("\n\n" + "#"*80)
    print("# CONTACT PATCH ENDPOINT TESTS (Protected)")
    print("#"*80)
    
    patch_without_token_passed, test_contact_id = test_contact_patch_without_token()
    results['contact_patch_without_token'] = patch_without_token_passed
    
    if admin_token and test_contact_id:
        results['contact_patch_with_token'] = test_contact_patch_with_token(admin_token, test_contact_id)
        results['contact_patch_nonexistent_id'] = test_contact_patch_nonexistent_id(admin_token)
        results['stats_after_marking_handled'] = test_stats_after_marking_handled(admin_token)
    else:
        print_result(False, "Skipping contact patch tests - no token or contact_id available")
        results['contact_patch_with_token'] = False
        results['contact_patch_nonexistent_id'] = False
        results['stats_after_marking_handled'] = False
    
    # Newsletter Tests (Public POST)
    print("\n\n" + "#"*80)
    print("# NEWSLETTER ENDPOINT TESTS (Public POST)")
    print("#"*80)
    
    results['newsletter_valid'] = test_newsletter_valid()
    results['newsletter_idempotent'] = test_newsletter_idempotent()
    results['newsletter_invalid_email'] = test_newsletter_invalid_email()
    results['newsletter_missing_email'] = test_newsletter_missing_email()
    
    # Newsletter GET (now protected)
    print("\n\n" + "#"*80)
    print("# NEWSLETTER GET ENDPOINT TESTS (Protected)")
    print("#"*80)
    
    results['newsletter_get_list_protected'] = test_newsletter_get_list_protected()
    if admin_token:
        results['newsletter_get_list_with_auth'] = test_newsletter_get_list_with_auth(admin_token)
    else:
        print_result(False, "Skipping newsletter_get_list_with_auth - no token available")
        results['newsletter_get_list_with_auth'] = False
    
    # Gallery Management Tests
    print("\n\n" + "#"*80)
    print("# GALLERY MANAGEMENT ENDPOINT TESTS")
    print("#"*80)
    
    # Test public GET /api/gallery
    gallery_passed, albums = test_gallery_get_public()
    results['gallery_get_public'] = gallery_passed
    
    # Test upload without auth
    results['gallery_upload_without_auth'] = test_gallery_upload_without_auth()
    
    if admin_token:
        # Test upload with auth
        upload_passed, uploaded_photo = test_gallery_upload_with_auth(admin_token)
        results['gallery_upload_with_auth'] = upload_passed
        
        if uploaded_photo:
            uploaded_photo_id = uploaded_photo['id']
            uploaded_photo_url = uploaded_photo['url']
            
            # Test serving uploaded file
            results['gallery_serve_uploaded_file'] = test_gallery_serve_uploaded_file(uploaded_photo_url)
            
            # Test set cover
            results['gallery_set_cover'] = test_gallery_set_cover(admin_token, uploaded_photo_id)
            
            # Test reorder
            results['gallery_reorder_photos'] = test_gallery_reorder_photos(admin_token, uploaded_photo_id)
            
            # Test partial reorder
            results['gallery_reorder_partial_list'] = test_gallery_reorder_partial_list(admin_token)
            
            # Test delete photo
            results['gallery_delete_photo'] = test_gallery_delete_photo(admin_token, uploaded_photo_id, uploaded_photo_url)
            
            # Test cover fallback
            results['gallery_cover_fallback'] = test_gallery_cover_fallback_after_delete(admin_token)
        else:
            print_result(False, "Skipping photo-dependent tests - upload failed")
            results['gallery_serve_uploaded_file'] = False
            results['gallery_set_cover'] = False
            results['gallery_reorder_photos'] = False
            results['gallery_reorder_partial_list'] = False
            results['gallery_delete_photo'] = False
            results['gallery_cover_fallback'] = False
        
        # Test validation
        results['gallery_upload_non_image'] = test_gallery_upload_non_image(admin_token)
        results['gallery_upload_large_file'] = test_gallery_upload_large_file(admin_token)
        
        # Test invalid IDs
        results['gallery_invalid_album_id'] = test_gallery_invalid_album_id(admin_token)
        results['gallery_invalid_photo_id'] = test_gallery_invalid_photo_id(admin_token)
        
        # Cleanup
        results['gallery_cleanup'] = test_gallery_cleanup_restore_original(admin_token)
    else:
        print_result(False, "Skipping gallery auth tests - no token available")
        results['gallery_upload_with_auth'] = False
        results['gallery_serve_uploaded_file'] = False
        results['gallery_set_cover'] = False
        results['gallery_reorder_photos'] = False
        results['gallery_reorder_partial_list'] = False
        results['gallery_delete_photo'] = False
        results['gallery_cover_fallback'] = False
        results['gallery_upload_non_image'] = False
        results['gallery_upload_large_file'] = False
        results['gallery_invalid_album_id'] = False
        results['gallery_invalid_photo_id'] = False
        results['gallery_cleanup'] = False
    
    # Summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {passed}/{total} tests passed")
    print(f"{'='*80}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
