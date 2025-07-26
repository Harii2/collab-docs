# Documents App

## Overview
The Documents app provides collaborative document editing functionality with features including document CRUD operations, collaborator management, and version history tracking.

## Features
- ✅ **Document CRUD** - Create, read, update, delete documents
- ✅ **Collaboration** - Add/remove collaborators with different permission levels
- ✅ **Version History** - Automatic versioning on document updates
- ✅ **Permission System** - VIEW, EDIT, ADMIN permission levels
- ✅ **JWT Authentication** - All endpoints protected with JWT tokens
- ✅ **Clean Architecture** - Organized with DTOs, Interactors, and Storage layers

## Architecture

### Clean Architecture Layers
```
API Layer (Views)
    ↓ DTOs
Interactor Layer (Business Logic)
    ↓ DTOs  
Storage Layer (Data Access)
    ↓
Models (Database)
```

### Folder Structure
```
documents/
├── docs/
│   └── api.md              # Complete API documentation
├── views/
│   ├── __init__.py         # View module exports
│   ├── document_views.py   # Document CRUD views
│   ├── collaborator_views.py # Collaborator management views
│   └── version_views.py    # Version history views
├── urls/
│   ├── __init__.py         # URL module registration
│   ├── document_urls.py    # Document endpoints
│   ├── collaborator_urls.py # Collaborator endpoints
│   └── version_urls.py     # Version endpoints
├── interactors/            # Business logic (in root/interactors/documents/)
├── models.py               # Database models
├── storage.py              # Data access layer
├── storage_interface.py    # Storage contracts
├── dtos.py                 # Data transfer objects
├── serializers.py          # API serialization
├── enums.py                # App-specific enums
└── validators.py           # Field validation
```

## Quick Start

### 1. Authentication
First, get a JWT token by logging in:
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### 2. Create a Document
```bash
curl -X POST http://localhost:8000/api/documents/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Document",
    "content": "Hello World!",
    "status": "DRAFT",
    "is_public": false
  }'
```

### 3. List Your Documents
```bash
curl -X GET http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Add a Collaborator
```bash
curl -X POST http://localhost:8000/api/documents/1/collaborators/add/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"user_id": 456, "permission": "EDIT"}'
```

## API Endpoints

### Documents
- `GET /api/documents/` - List documents
- `POST /api/documents/create/` - Create document
- `GET /api/documents/{id}/` - Get document
- `PUT /api/documents/{id}/update/` - Update document
- `DELETE /api/documents/{id}/delete/` - Delete document

### Collaborators
- `GET /api/documents/{id}/collaborators/` - List collaborators
- `POST /api/documents/{id}/collaborators/add/` - Add collaborator
- `PUT /api/documents/{id}/collaborators/{user_id}/update/` - Update permission
- `DELETE /api/documents/{id}/collaborators/{user_id}/remove/` - Remove collaborator

### Versions
- `GET /api/documents/{id}/versions/` - List versions
- `GET /api/documents/{id}/versions/{version}/` - Get specific version

## Permission System

| Permission | Can View | Can Edit | Can Manage Collaborators | Can Delete |
|------------|----------|----------|-------------------------|------------|
| `VIEW`     | ✅       | ❌       | ❌                      | ❌         |
| `EDIT`     | ✅       | ✅       | ❌                      | ❌         |
| `ADMIN`    | ✅       | ✅       | ✅                      | ✅         |

**Note:** Document owners always have full admin access.

## Models

### Document
- `title` - Document title (required)
- `content` - Document content (optional)
- `owner_id` - User ID of document owner
- `status` - DRAFT, PUBLISHED, or ARCHIVED
- `is_public` - Whether document is publicly accessible

### Collaborator
- `document` - ForeignKey to Document
- `user_id` - User ID of collaborator
- `permission` - VIEW, EDIT, or ADMIN
- `added_by_user_id` - User ID who added this collaborator

### DocumentVersion
- `document` - ForeignKey to Document
- `version_number` - Sequential version number
- `title` - Document title at this version
- `content` - Document content at this version
- `changed_by_user_id` - User ID who made the change
- `change_summary` - Description of changes

## Business Logic

### Document Access Rules
1. **Owners** can perform all operations
2. **Public documents** can be viewed by anyone
3. **Collaborators** have access based on their permission level
4. **Private documents** require explicit collaboration

### Automatic Versioning
- New version created on every document update
- Versions include title, content, and change metadata
- Version history preserved indefinitely

## Security Features
- ✅ **JWT Authentication** on all endpoints
- ✅ **Permission-based access control**
- ✅ **Owner and collaborator validation**
- ✅ **Input validation** with custom validators
- ✅ **Clean error responses**

## Performance Optimizations
- ✅ **Caching** - All models use AbstractDateTimeCacheModel with 2-hour TTL
- ✅ **Bulk operations** - No for loops in storage layer
- ✅ **Efficient queries** - Optimized database access patterns
- ✅ **Pagination** - List endpoints support limit/offset

## Testing
For complete API testing examples with curl commands, see [API Documentation](docs/api.md).

## Future Enhancements
- Real-time collaboration with WebSockets
- Document templates
- Advanced permission roles
- Document sharing links
- Export functionality
