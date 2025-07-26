# Documents API Documentation

## Overview
The Documents API provides endpoints for collaborative document editing with features including document CRUD operations, collaborator management, and version history tracking.

## Base URL
```
http://localhost:8000/api/documents/
```

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Document Endpoints

### 1. Create Document
**POST** `/api/documents/create/`

Creates a new document owned by the authenticated user.

**Request Body:**
```json
{
    "title": "My New Document",
    "content": "This is the initial content of the document.",
    "status": "DRAFT",
    "is_public": false
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/documents/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Project Proposal",
    "content": "# Project Overview\n\nThis document outlines our new project proposal...",
    "status": "DRAFT",
    "is_public": false
  }'
```

**Response (201 Created):**
```json
{
    "id": 1,
    "title": "Project Proposal",
    "content": "# Project Overview\n\nThis document outlines our new project proposal...",
    "owner_id": 123,
    "status": "DRAFT",
    "is_public": false,
    "created_at": "2025-01-26T18:27:54.123456Z",
    "updated_at": "2025-01-26T18:27:54.123456Z"
}
```

---

### 2. Get Document
**GET** `/api/documents/{document_id}/`

Retrieves a specific document if the user has access (owner, collaborator, or public document).

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/documents/1/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Project Proposal",
    "content": "# Project Overview\n\nThis document outlines our new project proposal...",
    "owner_id": 123,
    "status": "DRAFT",
    "is_public": false,
    "created_at": "2025-01-26T18:27:54.123456Z",
    "updated_at": "2025-01-26T18:27:54.123456Z"
}
```

---

### 3. Update Document
**PUT** `/api/documents/{document_id}/update/`

Updates a document. Only owners and collaborators with EDIT/ADMIN permissions can update. Automatically creates a new version.

**Request Body:**
```json
{
    "title": "Updated Project Proposal",
    "content": "# Updated Project Overview\n\nThis is the revised version...",
    "status": "PUBLISHED",
    "is_public": true
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/api/documents/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Project Proposal",
    "content": "# Updated Project Overview\n\nThis is the revised version with new insights...",
    "status": "PUBLISHED"
  }'
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Updated Project Proposal",
    "content": "# Updated Project Overview\n\nThis is the revised version with new insights...",
    "owner_id": 123,
    "status": "PUBLISHED",
    "is_public": false,
    "created_at": "2025-01-26T18:27:54.123456Z",
    "updated_at": "2025-01-26T18:35:12.789012Z"
}
```

---

### 4. Delete Document
**DELETE** `/api/documents/{document_id}/delete/`

Deletes a document. Only owners and collaborators with ADMIN permissions can delete.

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/documents/1/delete/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (204 No Content):**
```json
{
    "message": "Document deleted successfully"
}
```

---

### 5. List Documents
**GET** `/api/documents/`

Lists documents accessible to the authenticated user (owned documents and collaborations).

**Query Parameters:**
- `owner_id` (optional): Filter by owner ID
- `status` (optional): Filter by status (DRAFT, PUBLISHED, ARCHIVED)
- `is_public` (optional): Filter by public status (true/false)
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset (default: 0)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/api/documents/?status=PUBLISHED&limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Project Proposal",
        "content": "# Project Overview...",
        "owner_id": 123,
        "status": "PUBLISHED",
        "is_public": true,
        "created_at": "2025-01-26T18:27:54.123456Z",
        "updated_at": "2025-01-26T18:35:12.789012Z"
    },
    {
        "id": 2,
        "title": "Meeting Notes",
        "content": "## Team Meeting - Jan 26...",
        "owner_id": 456,
        "status": "PUBLISHED",
        "is_public": false,
        "created_at": "2025-01-26T19:15:30.456789Z",
        "updated_at": "2025-01-26T19:15:30.456789Z"
    }
]
```

---

## Collaborator Endpoints

### 1. Add Collaborator
**POST** `/api/documents/{document_id}/collaborators/add/`

Adds a collaborator to a document. Only owners and ADMIN collaborators can add collaborators.

**Request Body:**
```json
{
    "user_id": 456,
    "permission": "EDIT"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/documents/1/collaborators/add/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 456,
    "permission": "EDIT"
  }'
```

**Response (201 Created):**
```json
{
    "id": 1,
    "document_id": 1,
    "user_id": 456,
    "permission": "EDIT",
    "added_by_user_id": 123,
    "created_at": "2025-01-26T18:45:20.123456Z",
    "updated_at": "2025-01-26T18:45:20.123456Z"
}
```

---

### 2. Get Document Collaborators
**GET** `/api/documents/{document_id}/collaborators/`

Lists all collaborators for a document.

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/documents/1/collaborators/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "document_id": 1,
        "user_id": 456,
        "permission": "EDIT",
        "added_by_user_id": 123,
        "created_at": "2025-01-26T18:45:20.123456Z",
        "updated_at": "2025-01-26T18:45:20.123456Z"
    },
    {
        "id": 2,
        "document_id": 1,
        "user_id": 789,
        "permission": "VIEW",
        "added_by_user_id": 123,
        "created_at": "2025-01-26T19:10:15.789012Z",
        "updated_at": "2025-01-26T19:10:15.789012Z"
    }
]
```

---

### 3. Update Collaborator Permission
**PUT** `/api/documents/{document_id}/collaborators/{user_id}/update/`

Updates a collaborator's permission level.

**Request Body:**
```json
{
    "permission": "ADMIN"
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/api/documents/1/collaborators/456/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "permission": "ADMIN"
  }'
```

**Response (200 OK):**
```json
{
    "id": 1,
    "document_id": 1,
    "user_id": 456,
    "permission": "ADMIN",
    "added_by_user_id": 123,
    "created_at": "2025-01-26T18:45:20.123456Z",
    "updated_at": "2025-01-26T19:25:30.456789Z"
}
```

---

### 4. Remove Collaborator
**DELETE** `/api/documents/{document_id}/collaborators/{user_id}/remove/`

Removes a collaborator from a document.

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/documents/1/collaborators/456/remove/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (204 No Content):**
```json
{
    "message": "Collaborator removed successfully"
}
```

---

## Version History Endpoints

### 1. Get Document Versions
**GET** `/api/documents/{document_id}/versions/`

Lists all versions of a document in reverse chronological order.

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/documents/1/versions/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
[
    {
        "id": 3,
        "document_id": 1,
        "version_number": 3,
        "title": "Updated Project Proposal",
        "content": "# Updated Project Overview\n\nThis is the revised version...",
        "changed_by_user_id": 123,
        "change_summary": "Document updated",
        "created_at": "2025-01-26T19:35:12.789012Z",
        "updated_at": "2025-01-26T19:35:12.789012Z"
    },
    {
        "id": 2,
        "document_id": 1,
        "version_number": 2,
        "title": "Project Proposal",
        "content": "# Project Overview\n\nThis document outlines...",
        "changed_by_user_id": 456,
        "change_summary": "Document updated",
        "created_at": "2025-01-26T18:50:45.234567Z",
        "updated_at": "2025-01-26T18:50:45.234567Z"
    }
]
```

---

### 2. Get Specific Version
**GET** `/api/documents/{document_id}/versions/{version_number}/`

Retrieves a specific version of a document.

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/documents/1/versions/2/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
{
    "id": 2,
    "document_id": 1,
    "version_number": 2,
    "title": "Project Proposal",
    "content": "# Project Overview\n\nThis document outlines our project proposal with initial requirements...",
    "changed_by_user_id": 456,
    "change_summary": "Document updated",
    "created_at": "2025-01-26T18:50:45.234567Z",
    "updated_at": "2025-01-26T18:50:45.234567Z"
}
```

---

## Permission Types

| Permission | Description |
|------------|-------------|
| `VIEW` | Can view the document only |
| `EDIT` | Can view and edit the document |
| `ADMIN` | Can view, edit, manage collaborators, and delete |

## Document Status Types

| Status | Description |
|--------|-------------|
| `DRAFT` | Document is in draft state |
| `PUBLISHED` | Document is published and finalized |
| `ARCHIVED` | Document is archived |

---

## Error Responses

### 400 Bad Request
```json
{
    "title": ["This field is required."],
    "permission": ["Invalid permission type. Must be one of: VIEW, EDIT, ADMIN"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "error": "Document not found or access denied"
}
```

---

## Authentication Flow

1. **Login to get JWT token:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

2. **Use the token in subsequent requests:**
```bash
# Extract the access token from login response
export JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Use in API calls
curl -X GET http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

---

## Rate Limiting
- No rate limiting currently implemented
- Consider implementing rate limiting for production use

## Versioning
- API Version: v1
- All endpoints are stable and backward compatible
