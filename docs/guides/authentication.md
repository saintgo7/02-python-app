# Authentication Guide

## JWT Authentication
All endpoints (except registration and login) require JWT authentication.

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Using Token
Include the token in the Authorization header:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/items
```
