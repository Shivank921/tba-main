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
        "password": "BangaliCoimbatore@2026"
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

def main():
    print("\n" + "="*80)
    print("BACKEND API TESTING - Bengali Association Coimbatore")
    print(f"Base URL: {BASE_URL}")
    print("="*80)
    
    results = {}
    admin_token = None
    test_contact_id = None
    
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
