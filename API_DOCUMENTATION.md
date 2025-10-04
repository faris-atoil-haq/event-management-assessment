# Event Management API Documentation

This documentation covers all the available API endpoints for the Event Management System. All endpoints require authentication unless otherwise specified.

## Base URL
```
https://your-domain.com/api/
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Authentication Endpoints

#### 1. Login
**POST** `/api/auth/login/`

Authenticate a user and receive JWT tokens.

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response (200 OK):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access_token_expires_at": "2024-01-01T12:00:00Z",
    "refresh_token_expires_at": "2024-01-08T12:00:00Z",
    "access_token_expires_in": 3600,
    "refresh_token_expires_in": 604800
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "No active account found with the given credentials"
}
```

#### 2. Refresh Token
**POST** `/api/auth/refresh/`

Refresh an expired access token using a valid refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access_token_expires_at": "2024-01-01T13:00:00Z",
    "access_token_expires_in": 3600
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

## User Endpoints

#### 3. User Profile
**GET** `/api/profile/`

Get the current authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Event Endpoints

#### 4. List Events / Create Event
**GET/POST** `/api/events/`

**GET** - Retrieve all events ordered by creation date (newest first)
**POST** - Create a new event (authenticated users only)

##### GET Request

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Tech Conference 2024",
        "description": "Annual technology conference featuring latest innovations",
        "date_start": "2024-02-15T09:00:00Z",
        "date_end": "2024-02-15T18:00:00Z",
        "venue": "Convention Center Hall A",
        "capacity": 500,
        "organizer": "john_doe",
        "created_at": "2024-01-01T10:00:00Z"
    },
    {
        "id": 2,
        "title": "Marketing Workshop",
        "description": "Learn effective marketing strategies",
        "date_start": "2024-02-20T14:00:00Z",
        "date_end": "2024-02-20T17:00:00Z",
        "venue": "Training Room B",
        "capacity": 50,
        "organizer": "jane_smith",
        "created_at": "2024-01-01T09:00:00Z"
    }
]
```

##### POST Request

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "Web Development Bootcamp",
    "description": "Intensive 3-day web development training",
    "date_start": "2024-03-01T09:00:00Z",
    "date_end": "2024-03-03T17:00:00Z",
    "venue": "Tech Hub Room 301",
    "capacity": 30
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "title": "Web Development Bootcamp",
    "description": "Intensive 3-day web development training",
    "date_start": "2024-03-01T09:00:00Z",
    "date_end": "2024-03-03T17:00:00Z",
    "venue": "Tech Hub Room 301",
    "capacity": 30,
    "organizer": "john_doe",
    "created_at": "2024-01-01T11:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
    "non_field_errors": [
        "Start date must be before end date"
    ]
}
```

#### 5. Event Detail
**GET/PUT/PATCH/DELETE** `/api/events/<event_id>/`

Retrieve, update, or delete a specific event. Only the event organizer can update or delete their events.

##### GET Request

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference featuring latest innovations",
    "date_start": "2024-02-15T09:00:00Z",
    "date_end": "2024-02-15T18:00:00Z",
    "venue": "Convention Center Hall A",
    "capacity": 500,
    "organizer": "john_doe",
    "created_at": "2024-01-01T10:00:00Z"
}
```

##### PUT Request (Full Update)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "Tech Conference 2024 - Updated",
    "description": "Annual technology conference with new speakers",
    "date_start": "2024-02-15T09:00:00Z",
    "date_end": "2024-02-15T19:00:00Z",
    "venue": "Convention Center Hall A",
    "capacity": 600
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Tech Conference 2024 - Updated",
    "description": "Annual technology conference with new speakers",
    "date_start": "2024-02-15T09:00:00Z",
    "date_end": "2024-02-15T19:00:00Z",
    "venue": "Convention Center Hall A",
    "capacity": 600,
    "organizer": "john_doe",
    "created_at": "2024-01-01T10:00:00Z"
}
```

##### PATCH Request (Partial Update)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "capacity": 550
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference featuring latest innovations",
    "date_start": "2024-02-15T09:00:00Z",
    "date_end": "2024-02-15T18:00:00Z",
    "venue": "Convention Center Hall A",
    "capacity": 550,
    "organizer": "john_doe",
    "created_at": "2024-01-01T10:00:00Z"
}
```

##### DELETE Request

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content):**
```
(No response body)
```

**Error Response (403 Forbidden):**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

**Error Response (404 Not Found):**
```json
{
    "detail": "Not found."
}
```

#### 6. Register to Event
**POST** `/api/events/<event_id>/register/`

Register the authenticated user as an attendee for a specific event.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Successfully registered to Tech Conference 2024",
    "event_id": 1
}
```

**Error Response (404 Not Found):**
```json
{
    "error": "Event not found"
}
```

#### 7. My Events
**GET** `/api/my-events/`

Retrieve all events that the authenticated user has registered for as an attendee.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Tech Conference 2024",
        "description": "Annual technology conference featuring latest innovations",
        "date_start": "2024-02-15T09:00:00Z",
        "date_end": "2024-02-15T18:00:00Z",
        "venue": "Convention Center Hall A",
        "capacity": 500,
        "organizer": "john_doe",
        "created_at": "2024-01-01T10:00:00Z"
    }
]
```

**Response (200 OK - No registrations):**
```json
[]
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required or token invalid |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

## Common Error Response Format

```json
{
    "detail": "Error message description",
    "code": "error_code" // Optional
}
```

Or for validation errors:

```json
{
    "field_name": [
        "Error message for this field"
    ],
    "non_field_errors": [
        "General validation error"
    ]
}
```

## Rate Limiting

Currently, there are no rate limits implemented, but it's recommended to implement reasonable request limits in production environments.

## API Versioning

This is version 1 of the API. Future versions may be introduced with different URL patterns (e.g., `/api/v2/`).

## Notes

1. All datetime fields are in ISO 8601 format with UTC timezone
2. All requests and responses use JSON format
3. Authentication tokens have configurable expiration times
4. Event organizers have full CRUD permissions on their events
5. All users can view events and register as attendees
6. The system automatically tracks attendee registrations with "pending" status