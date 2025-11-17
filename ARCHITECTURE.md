# 🏗️ Architecture & Technology Stack

Complete technical documentation of the system architecture and technology decisions.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Architecture](#data-architecture)
6. [Infrastructure Architecture](#infrastructure-architecture)
7. [Security Architecture](#security-architecture)
8. [Scalability Architecture](#scalability-architecture)
9. [Design Patterns](#design-patterns)
10. [Performance Optimization](#performance-optimization)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
├─────────────────────────┬───────────────────────────────────────┤
│ React.js Frontend       │ Vue.js Frontend                       │
│ (FastAPI Clients)       │ (Django Clients)                      │
│ TypeScript + Tailwind   │ TypeScript + Tailwind                 │
└─────────────────────────┴───────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │ API Gateway / ALB  │
                    │ Load Balancing     │
                    │ SSL/TLS            │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┼────────────────────┐
        │                     │                    │
   ┌────▼─────┐         ┌────▼─────┐        ┌────▼──────┐
   │ FastAPI  │         │  Django  │        │ AI/ML API │
   │ Projects │         │ Projects │        │ Projects  │
   │ (01-10)  │         │ (11-20)  │        │ (21-60)   │
   └────┬─────┘         └────┬─────┘        └────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼──────┐        ┌────▼──────┐      ┌────▼───────┐
   │PostgreSQL │        │ Redis     │      │S3 Storage  │
   │ Database  │        │ Cache     │      │Static Files│
   └───────────┘        └───────────┘      └────────────┘
```

### Component Interaction Flow

```
Client Request
    │
    ▼
CDN / CloudFront (Static Assets)
    │
    ▼
Application Load Balancer (ALB)
    │
    ├─▶ Route to FastAPI (WebSockets, Real-time)
    ├─▶ Route to Django (Traditional REST)
    └─▶ Route to AI/ML Services (Heavy Processing)
    │
    ▼
Application Server
    │
    ├─▶ Authentication (JWT)
    ├─▶ Rate Limiting
    ├─▶ Request Validation
    │
    ▼
Business Logic Layer
    │
    ├─▶ Check Cache (Redis)
    ├─▶ Query Database (PostgreSQL)
    └─▶ External API Calls
    │
    ▼
Response Formatting
    │
    ▼
Client
```

---

## Technology Stack

### Backend Services (60 Applications)

#### FastAPI (10 Projects: 01-10)

**Why FastAPI?**
- Modern async Python framework (2x-3x faster than Flask/Django)
- Built-in OpenAPI documentation
- Automatic request validation via Pydantic
- High performance due to async/await
- Type hints for better IDE support
- Perfect for SaaS applications

```python
# Typical FastAPI project structure
fastapi/
├── main.py              # Application entry point
├── app/
│   ├── core/           # Core utilities (db, security)
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic validation schemas
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic
│   └── middleware/     # Request/response middleware
├── tests/              # Test suite
└── requirements.txt    # Dependencies
```

**Key Features:**
- JWT authentication with bcrypt
- SQLAlchemy ORM for database
- Redis caching with async support
- WebSocket support for real-time
- GraphQL API option
- Advanced filtering and pagination
- Rate limiting
- CORS configuration

#### Django (10 Projects: 11-20)

**Why Django?**
- Mature, battle-tested framework (18+ years)
- Built-in admin interface for data management
- Django ORM with advanced QuerySets
- Django REST Framework for APIs
- Multi-tenancy support
- Excellent security defaults
- Great for PaaS applications

```python
# Typical Django project structure
django/
├── manage.py           # Management script
├── project/
│   ├── settings.py     # Configuration
│   ├── urls.py         # URL routing
│   └── wsgi.py         # WSGI application
├── app/
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── serializers.py  # DRF serializers
│   ├── viewsets.py     # REST endpoints
│   ├── managers.py     # Custom QuerySet managers
│   └── signals.py      # Event handlers
├── tests/              # Test suite
└── requirements.txt    # Dependencies
```

**Key Features:**
- Advanced ORM with custom managers
- DRF Spectacular for API documentation
- Caching layer with Redis
- Custom permission classes
- Signal handlers for events
- Admin interface customization
- Multi-database support
- Transaction management

#### AI/ML Services (40 Projects: 21-60)

**PyTorch (21-30)** - Research & Flexibility

```python
# Model training pipeline
class ObjectDetectionTrainer:
    def __init__(self):
        self.model = YOLOv8()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.optimizer = torch.optim.Adam(self.model.parameters())

    def train_batch(self, images, targets):
        # Forward pass
        predictions = self.model(images)
        loss = self.compute_loss(predictions, targets)

        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
```

**TensorFlow (31-40)** - Production & Optimization

```python
# Model inference with optimization
class TrafficSignDetector:
    def __init__(self):
        self.model = tf.keras.models.load_model('model.h5')
        self.model = tf.lite.TFLiteConverter.from_keras_model(self.model).convert()

    def predict(self, image):
        # Preprocess
        image = self.preprocess(image)

        # Inference
        interpreter = tf.lite.Interpreter(self.model)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()

        return interpreter.get_tensor(output_details[0]['index'])
```

**Monetization Tools (41-60)** - Business Logic

```python
# Typical tool structure
class StockPriceAnalyzer(FastAPI):
    async def analyze(self, symbol: str):
        # Fetch data
        data = await self.fetch_stock_data(symbol)

        # Analyze
        indicators = self.calculate_indicators(data)

        # Predict
        prediction = await self.predict_price(data)

        # Format response
        return {
            "symbol": symbol,
            "indicators": indicators,
            "prediction": prediction,
            "timestamp": datetime.now()
        }
```

### Frontend Technologies

#### React.js (For FastAPI)

```
react-app/
├── src/
│   ├── pages/          # Page components
│   ├── components/     # Reusable components
│   ├── stores/         # Zustand state management
│   ├── api/            # API integration layer
│   ├── types/          # TypeScript interfaces
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Utility functions
│   └── styles/         # CSS stylesheets
├── public/             # Static files
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
└── vite.config.ts      # Vite bundler config
```

**Key Libraries:**
- **React 18**: Component-based UI
- **TypeScript**: Type safety
- **Zustand**: Lightweight state management
- **React Query**: Server state management
- **Axios**: HTTP client with JWT
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **React Hot Toast**: Toast notifications

**Architecture Pattern:**
```
Component → Hook (useAuth, useFetch)
           → Zustand Store (authStore)
           → API Client (axios with JWT)
           → Backend (FastAPI)
```

#### Vue.js (For Django)

```
vue-app/
├── src/
│   ├── pages/          # Page components
│   ├── components/     # Reusable components
│   ├── stores/         # Pinia state management
│   ├── api/            # API integration
│   ├── types/          # TypeScript interfaces
│   ├── composables/    # Composition API logic
│   ├── utils/          # Utilities
│   └── styles/         # Styles
├── public/             # Static files
├── package.json        # Dependencies
└── vite.config.ts      # Vite config
```

**Key Libraries:**
- **Vue 3**: Progressive framework
- **Composition API**: Reactive logic
- **Pinia**: State management
- **Axios**: HTTP client
- **Vue Router**: Routing
- **Tailwind CSS**: Styling

### Database Technologies

#### PostgreSQL (Production)

```sql
-- Connection pooling
-- max_connections: 200
-- shared_buffers: 256MB
-- effective_cache_size: 1GB

-- Typical schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Row-level security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY select_own_data ON users
    FOR SELECT USING (auth.uid() = id);
```

**Production Considerations:**
- Automated backups (daily)
- Multi-AZ replication
- Connection pooling (PgBouncer)
- Encryption at rest (KMS)
- SSL/TLS in transit
- Query optimization
- Index management
- Vacuum and analyze

#### SQLite (Development)

```python
# Development-only configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

**Advantages:**
- Zero setup
- File-based
- Perfect for local development
- No background service needed

#### Redis (Caching & Real-time)

```python
# Cache configuration
CACHE_CONFIG = {
    'default': {
        'BACKEND': 'redis.Redis',
        'LOCATION': 'redis://localhost:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'rediscluster.RedisCluster',
            'CONNECTION_POOL_CLASS': 'rediscluster.connection.ClusterConnectionPool',
        }
    }
}

# Cache usage patterns
await redis.set(f"user:{user_id}:profile", json.dumps(profile), ex=3600)
profile = await redis.get(f"user:{user_id}:profile")
await redis.delete(f"user:{user_id}:profile")  # Invalidation
```

**Use Cases:**
- Session storage
- API response caching
- Rate limiting counters
- Real-time data (WebSocket state)
- Pub/Sub messaging

---

## Backend Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                         │
│  - HTTP Endpoints                                       │
│  - Request/Response Formatting                          │
│  - Swagger/OpenAPI Documentation                        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           APPLICATION LAYER                             │
│  - Business Logic                                       │
│  - Data Validation                                      │
│  - Services & Use Cases                                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│          PERSISTENCE LAYER                              │
│  - ORM (SQLAlchemy / Django ORM)                        │
│  - Database Abstraction                                 │
│  - Migrations                                           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│          DATA LAYER                                     │
│  - PostgreSQL Database                                  │
│  - Redis Cache                                          │
│  - S3 Storage                                           │
└─────────────────────────────────────────────────────────┘
```

### FastAPI Service Example

```python
# Layer 1: Route (Presentation)
@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return await item_service.create(item, db)

# Layer 2: Service (Application)
class ItemService:
    async def create(self, item: ItemCreate, db: Session):
        # Validate
        if not self.validate(item):
            raise ValueError("Invalid item")

        # Create
        db_item = Item(**item.dict())

        # Save
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        # Cache
        await self.cache.set(f"item:{db_item.id}", db_item)

        return db_item

# Layer 3: Repository (Persistence)
class ItemRepository:
    def get(self, item_id: int, db: Session):
        return db.query(Item).filter(Item.id == item_id).first()

# Layer 4: Model (Data)
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
```

### Authentication Flow

```
User Login Request
    │
    ├─▶ Hash password: bcrypt.hashpw(password, salt=bcrypt.gensalt())
    │
    ├─▶ Verify against stored hash
    │
    ├─▶ Generate JWT token:
    │   - Header: {alg: HS256, typ: JWT}
    │   - Payload: {sub: user_id, exp: timestamp, iat: timestamp}
    │   - Signature: HMAC-SHA256(header.payload, secret_key)
    │
    ├─▶ Return: {access_token, token_type: "bearer", expires_in}
    │
Client stores token in localStorage
    │
    ├─▶ Every API request includes:
    │   Authorization: Bearer <token>
    │
Server verifies token:
    │
    ├─▶ Decode using secret key
    ├─▶ Verify signature
    ├─▶ Check expiration
    ├─▶ Extract user_id from claims
    │
    ▼
Request processed as authenticated user
```

---

## Frontend Architecture

### Component Hierarchy

```
App.tsx
├── Navbar
│   └── User Menu
├── Router
│   ├── LoginPage
│   │   ├── LoginForm
│   │   └── SignupForm
│   ├── DashboardPage
│   │   ├── StatsCard (x3)
│   │   ├── ActivityFeed
│   │   └── Charts
│   └── ItemsPage
│       ├── ItemsList
│       │   └── ItemCard (x*)
│       └── CreateItemForm
└── Toast Notifications
```

### State Management (React + Zustand)

```typescript
// Global auth state
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { user, access_token } = response.data;

    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));

    set({ user, token: access_token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },
}));

// Usage in component
function LoginPage() {
  const { login } = useAuthStore();

  const handleSubmit = async (email, password) => {
    await login(email, password);
    navigate('/dashboard');
  };
}
```

### API Integration

```typescript
// Axios instance with JWT interceptor
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

---

## Data Architecture

### Database Schema Design

```sql
-- User Management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_status ON items(status);
CREATE INDEX idx_items_created_at ON items(created_at DESC);

-- Activity logging
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource VARCHAR(100),
    resource_id INTEGER,
    changes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id_created ON audit_logs(user_id, created_at DESC);
```

### Data Flow

```
User Input (Form)
    │
    ▼
Validation (Frontend)
    │
    ▼
API Request (Axios + JWT)
    │
    ▼
Server Validation (Pydantic/Serializer)
    │
    ▼
Business Logic (Service)
    │
    ├─▶ Check Cache (Redis)
    │   └─▶ Cache Hit: Return cached data
    │
    ├─▶ Query Database (PostgreSQL)
    │   └─▶ Execute SQL, Transform to ORM
    │
    ├─▶ Process Data
    │   └─▶ Transform, Aggregate, Calculate
    │
    ├─▶ Store Cache (Redis, ex=3600)
    │
    ▼
Response Formatting (Serialization)
    │
    ▼
HTTP Response (JSON)
    │
    ▼
Client (Axios + Zustand)
    │
    ▼
UI Update (React/Vue)
    │
    ▼
Display to User
```

---

## Infrastructure Architecture

### AWS Architecture

```
┌─────────────────────────────────────────────────────────┐
│         INTERNET & DNS                                  │
│         Route 53 (DNS)                                  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│         EDGE LAYER                                      │
│         CloudFront (CDN)                                │
│         - Static assets caching                         │
│         - Global distribution                           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│         LOAD BALANCING                                  │
│         Application Load Balancer (ALB)                 │
│         - Request routing                               │
│         - SSL/TLS termination                           │
│         - Health checks                                 │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐     ┌──▼────┐    ┌───▼───┐
   │  EC2    │     │ EC2   │    │ EC2   │
   │Instance │     │Instance    │Instance
   │    1    │     │    2  │    │   3   │
   └────┬────┘     └──┬────┘    └───┬───┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────┼────────────┐
        │             │            │
   ┌────▼────┐  ┌────▼───┐  ┌────▼─────┐
   │PostgreSQL    │ ElastiCache │S3 Bucket
   │  RDS (Multi) │  Redis      │ Static
   │  with backup │  with auth  │ Files
   └─────────────┘  └──────────┘  └──────┘
```

### Terraform Infrastructure

```hcl
# Main infrastructure as code
terraform/
├── main.tf              # Provider and backend
├── vpc.tf              # Network configuration
├── rds.tf              # Database setup
├── redis.tf            # Cache setup
├── security.tf         # Security groups
├── iam.tf              # Roles and policies
├── variables.tf        # Input variables
├── outputs.tf          # Output values
│
└── modules/
    ├── iam/
    │   ├── main.tf
    │   └── variables.tf
    ├── elastic_beanstalk/
    └── alb/
```

---

## Security Architecture

### Authentication & Authorization

```python
# JWT Token Structure
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-id-123",
    "email": "user@example.com",
    "iat": 1234567890,
    "exp": 1234571490  # 1 hour expiration
  },
  "signature": "HMAC-SHA256(...)"
}
```

### Rate Limiting

```python
# Sliding window rate limiter
class RateLimiter:
    def __init__(self, redis_client, rate: int = 100, window: int = 60):
        self.redis = redis_client
        self.rate = rate          # requests
        self.window = window      # seconds

    async def is_allowed(self, user_id: str) -> bool:
        key = f"rate_limit:{user_id}"
        current = await self.redis.incr(key)

        if current == 1:
            await self.redis.expire(key, self.window)

        return current <= self.rate
```

### Input Validation

```python
# Pydantic validation
class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!",
                "first_name": "John"
            }
        }

# Usage in endpoint
@app.post("/users")
async def create_user(user: UserCreate):
    # user is automatically validated
    # If invalid, returns 422 with error details
```

---

## Scalability Architecture

### Horizontal Scaling

```
Load Balancer
    │
    ├─▶ Instance 1 (Container)
    ├─▶ Instance 2 (Container)
    ├─▶ Instance 3 (Container)
    └─▶ Instance N (Auto-scaling)
```

**Auto-scaling Rules:**
- Scale up when: CPU > 70% for 2 minutes
- Scale down when: CPU < 30% for 5 minutes
- Min instances: 2 (availability)
- Max instances: 10 (cost control)

### Caching Strategy

```
Cache Layers (from fastest to slowest)
│
├─▶ L1: Browser Cache
│   └─ Static assets (images, CSS, JS)
│   └─ Duration: 1 week
│
├─▶ L2: Redis Cache
│   └─ API responses
│   └─ Database query results
│   └─ Session data
│   └─ Duration: 5 minutes - 1 hour
│
├─▶ L3: Database Query Cache
│   └─ PostgreSQL query optimization
│   └─ Index usage
│   └─ Connection pooling
│
└─▶ L4: Database (Persistent)
    └─ Source of truth
    └─ Slow but reliable
```

### Database Optimization

```python
# Query optimization patterns

# 1. Use select_related for foreign keys
items = Item.objects.select_related('user').all()

# 2. Use prefetch_related for reverse relations
users = User.objects.prefetch_related('items').all()

# 3. Use only() to fetch specific fields
users = User.objects.only('id', 'email')

# 4. Use values() to get dictionaries instead of objects
data = Item.objects.values('id', 'title')

# 5. Add indexes for frequently queried fields
class Item(Base):
    title = Column(String, index=True)
    user_id = Column(Integer, index=True)

# 6. Use database-level filtering
items = session.query(Item).filter(Item.status == 'active')
```

---

## Design Patterns

### Service Pattern

```python
# Separation of concerns
class ItemService:
    def __init__(self, db: Session, cache: Redis):
        self.db = db
        self.cache = cache

    async def get_item(self, item_id: int) -> Item:
        # Try cache first
        cached = await self.cache.get(f"item:{item_id}")
        if cached:
            return Item(**json.loads(cached))

        # Query database
        item = self.db.query(Item).get(item_id)

        # Cache result
        await self.cache.set(f"item:{item_id}", item.json(), ex=3600)

        return item
```

### Repository Pattern

```python
# Abstract data access
class Repository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, id: int) -> Optional[T]:
        return self.db.query(self.model).get(id)

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        return instance
```

### Dependency Injection

```python
# Loose coupling
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis)
):
    return await ItemService(db, cache).create(item)
```

---

## Performance Optimization

### Frontend Optimization

```
Bundle Size Reduction:
├─ Code splitting by route
├─ Lazy loading components
├─ Minification (Vite handles this)
├─ Tree shaking (Remove unused code)
└─ Compression (gzip, brotli)

Performance Metrics:
├─ Largest Contentful Paint (LCP): < 2.5s
├─ First Input Delay (FID): < 100ms
├─ Cumulative Layout Shift (CLS): < 0.1
└─ Time to First Byte (TTFB): < 600ms
```

### Backend Optimization

```python
# Query optimization example
# SLOW: N+1 query problem
users = User.query.all()
for user in users:
    print(user.items)  # Each iteration = new query!

# FAST: Join query
users = User.query.options(
    joinedload(User.items)
).all()

# METRICS:
# Before: 1000 queries
# After: 1 query with join
```

### Database Optimization

```sql
-- Connection pooling
SET max_connections = 200;
SET shared_buffers = '256MB';
SET effective_cache_size = '1GB';

-- Query optimization
EXPLAIN ANALYZE
SELECT u.id, COUNT(i.id) as item_count
FROM users u
LEFT JOIN items i ON u.id = i.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id;

-- Index strategy
CREATE INDEX idx_items_user_status
ON items(user_id, status)
WHERE status != 'deleted';
```

---

## Monitoring & Observability

### Application Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Usage
@app.get("/items")
async def list_items():
    request_count.labels(method="GET", endpoint="/items").inc()
    # ...
```

### Logging Strategy

```python
import logging

logger = logging.getLogger(__name__)

logger.info("User logged in", extra={
    "user_id": user.id,
    "timestamp": datetime.now(),
    "ip_address": request.client.host
})

logger.error("Database connection failed", exc_info=True)
```

### Health Checks

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database
        await db.execute("SELECT 1")

        # Check cache
        await redis.ping()

        return {
            "status": "healthy",
            "database": "ok",
            "cache": "ok"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503
```

---

## Summary

This architecture provides:

✅ **Scalability**: Horizontal scaling with load balancing
✅ **Reliability**: Multi-AZ redundancy and backups
✅ **Security**: JWT auth, encryption, rate limiting
✅ **Performance**: Caching, query optimization, CDN
✅ **Maintainability**: Layered architecture, design patterns
✅ **Observability**: Monitoring, logging, health checks
✅ **Cost Efficiency**: Auto-scaling, resource optimization

---

**End of Architecture Documentation**
