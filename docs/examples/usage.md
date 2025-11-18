# Usage Examples

## Python Client
```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/auth/login',
    json={'email': 'user@example.com', 'password': 'password123'}
)
token = response.json()['access_token']

# Get items
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/items', headers=headers)
items = response.json()
```

## JavaScript Client
```javascript
// Login
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@example.com', password: 'password123'})
});
const {access_token} = await response.json();

// Get items
const itemsResponse = await fetch('http://localhost:8000/items', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const items = await itemsResponse.json();
```
