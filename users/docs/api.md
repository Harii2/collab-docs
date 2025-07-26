# Users App - API Documentation

## Base URL
```
http://localhost:8000/api/users/
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 1. User Registration

**Endpoint:** `POST /api/users/register/`  
**Authentication:** Not required  
**Description:** Register a new user account

### Request Payload
```json
{
  "email": "john.doe@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "password2": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Response (201 Created)
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "",
    "full_name": "John Doe",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "message": "User registered successfully. Please login to continue."
}
```

### Error Response (400 Bad Request)
```json
{
  "email": ["A user with this email already exists."],
  "password": ["Password fields didn't match."]
}
```

---

## 2. User Login

**Endpoint:** `POST /api/users/login/`  
**Authentication:** Not required  
**Description:** Login and get JWT tokens

### Request Payload
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

### Response (200 OK)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  }
}
```

### Error Response (401 Unauthorized)
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

## 3. Token Refresh

**Endpoint:** `POST /api/users/login/refresh/`  
**Authentication:** Not required  
**Description:** Refresh access token using refresh token

### Request Payload
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Response (200 OK)
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 4. Get User Profile

**Endpoint:** `GET /api/users/profile/`  
**Authentication:** Required  
**Description:** Get current user's profile information

### Request Headers
```
Authorization: Bearer <access_token>
```

### Response (200 OK)
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer passionate about collaborative tools.",
  "full_name": "John Doe",
  "date_joined": "2024-01-15T10:30:00Z"
}
```

---

## 5. Update User Profile

**Endpoint:** `PUT /api/users/profile/`  
**Authentication:** Required  
**Description:** Update user profile information

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request Payload
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Full-stack developer with 5+ years experience in web development."
}
```

### Response (200 OK)
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "bio": "Full-stack developer with 5+ years experience in web development.",
    "full_name": "John Smith",
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "message": "Profile updated successfully."
}
```

---

## 6. Get Current User Info

**Endpoint:** `GET /api/users/info/`  
**Authentication:** Required  
**Description:** Get current user information (alternative to profile endpoint)

### Request Headers
```
Authorization: Bearer <access_token>
```

### Response (200 OK)
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "bio": "Full-stack developer with 5+ years experience.",
    "full_name": "John Smith",
    "date_joined": "2024-01-15T10:30:00Z"
  }
}
```

---

## 7. Change Password

**Endpoint:** `POST /api/users/change-password/`  
**Authentication:** Required  
**Description:** Change user password

### Request Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request Payload
```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewSecurePassword456!",
  "confirm_password": "NewSecurePassword456!"
}
```

### Response (200 OK)
```json
{
  "message": "Password changed successfully."
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Old password is incorrect."
}
```

---

## 8. Check Email Availability

**Endpoint:** `GET /api/users/check-email/`  
**Authentication:** Not required  
**Description:** Check if email is available for registration

### Query Parameters
- `email` (required): Email address to check

### Example Request
```
GET /api/users/check-email/?email=test@example.com
```

### Response (200 OK)
```json
{
  "email": "test@example.com",
  "available": true
}
```

### Response (Email Taken)
```json
{
  "email": "john.doe@example.com",
  "available": false
}
```

---

## 9. Check Username Availability

**Endpoint:** `GET /api/users/check-username/`  
**Authentication:** Not required  
**Description:** Check if username is available for registration

### Query Parameters
- `username` (required): Username to check

### Example Request
```
GET /api/users/check-username/?username=johndoe
```

### Response (200 OK)
```json
{
  "username": "newuser",
  "available": true
}
```

### Response (Username Taken)
```json
{
  "username": "johndoe",
  "available": false
}
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "field_name": ["Error message describing the issue."]
}
```

#### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

#### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

---

## JWT Token Structure

### Access Token Claims
```json
{
  "token_type": "access",
  "exp": 1642248600,
  "iat": 1642245000,
  "jti": "abc123...",
  "user_id": 1,
  "email": "john.doe@example.com",
  "username": "johndoe",
  "full_name": "John Doe"
}
```

### Token Lifetimes
- **Access Token**: 60 minutes
- **Refresh Token**: 7 days

---

## Testing Examples

### Using cURL

#### Register User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "password2": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

#### Get Profile
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Using Python Requests

```python
import requests

# Register
response = requests.post('http://localhost:8000/api/users/register/', json={
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "password2": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
})

# Login
response = requests.post('http://localhost:8000/api/users/login/', json={
    "email": "test@example.com",
    "password": "TestPassword123!"
})
tokens = response.json()

# Get Profile
headers = {'Authorization': f'Bearer {tokens["access"]}'}
response = requests.get('http://localhost:8000/api/users/profile/', headers=headers)
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Email addresses must be unique across the system
- Usernames must be unique across the system
- Passwords must meet Django's default validation requirements
- JWT tokens are stateless and contain user information
- Refresh tokens automatically rotate on use (if configured)
