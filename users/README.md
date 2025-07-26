# Users App

## Overview
The Users app handles all user authentication, registration, and profile management functionality for the Collaborative Document Editing Platform. It provides a complete JWT-based authentication system with custom user model and comprehensive API endpoints.

## Responsibilities

### 🔐 Authentication & Authorization
- User registration with email-based authentication
- JWT token-based login system
- Token refresh mechanism
- Secure password management

### 👤 User Profile Management
- Custom user model with extended fields
- Profile information updates
- User information retrieval
- Account management features

### ✅ Validation & Security
- Email and username uniqueness validation
- Password strength validation
- Secure password change functionality
- Input validation and sanitization

## Features

### Custom User Model
- **Email as primary identifier** (instead of username)
- **Extended user fields**: bio, first_name, last_name
- **Helper methods**: get_full_name(), get_short_name()
- **Django admin integration**

### JWT Authentication
- **Access tokens** (60 minutes lifetime)
- **Refresh tokens** (7 days lifetime)
- **Custom claims** (email, username, full_name)
- **Automatic token rotation**

### API Endpoints
- **8 comprehensive endpoints** covering all user operations
- **RESTful design** with proper HTTP methods
- **Detailed error handling** and validation
- **Consistent response format**

## Available APIs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/register/` | User registration | No |
| POST | `/api/users/login/` | JWT login | No |
| POST | `/api/users/login/refresh/` | Token refresh | No |
| GET/PUT | `/api/users/profile/` | Profile view/update | Yes |
| GET | `/api/users/info/` | Current user info | Yes |
| POST | `/api/users/change-password/` | Change password | Yes |
| GET | `/api/users/check-email/` | Check email availability | No |
| GET | `/api/users/check-username/` | Check username availability | No |

## Quick Start

1. **Add to Django settings**:
```python
INSTALLED_APPS = [
    # ... other apps
    'users',
]

AUTH_USER_MODEL = 'users.CustomUser'
```

2. **Run migrations**:
```bash
python manage.py makemigrations users
python manage.py migrate
```

3. **Include URLs**:
```python
# In main urls.py
urlpatterns = [
    path('api/users/', include('users.urls')),
]
```

## Dependencies
- Django REST Framework
- SimpleJWT
- Django (Custom User Model)

## File Structure
```
users/
├── __init__.py
├── admin.py          # Django admin configuration
├── apps.py           # App configuration
├── models.py         # CustomUser model
├── serializers.py    # DRF serializers
├── views.py          # API views
├── urls.py           # URL routing
├── README.md         # This file
└── docs/
    └── api.md        # Detailed API documentation
```

## Next Steps
- Configure Django settings
- Run database migrations
- Test API endpoints
- Integrate with frontend

For detailed API documentation with request/response examples, see [docs/api.md](docs/api.md).
