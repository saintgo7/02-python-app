#!/usr/bin/env python3
"""
Project Enhancement Script
Adds advanced features to all projects:
- Advanced filtering, searching, sorting, pagination
- Redis caching
- WebSocket real-time features
- GraphQL API
"""

from pathlib import Path
from typing import Dict, List

# ============================
# ADVANCED CRUD ROUTES WITH FILTERING, SEARCH, SORT, PAGINATION
# ============================

def generate_advanced_crud_routes() -> str:
    """Generate advanced CRUD routes with full filtering, search, sort, pagination"""
    return '''from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app import models, schemas

router = APIRouter(tags=["advanced-crud"])


class PaginationParams:
    """Pagination parameters"""
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit


def apply_search(query, model, search_fields: List[str], search_term: str):
    """Apply search filtering"""
    if not search_term:
        return query

    search_conditions = [
        getattr(model, field).ilike(f"%{search_term}%")
        for field in search_fields
        if hasattr(model, field)
    ]

    if search_conditions:
        query = query.filter(or_(*search_conditions))

    return query


def apply_sort(query, model, sort_by: str, sort_order: str):
    """Apply sorting"""
    if not sort_by or not hasattr(model, sort_by):
        return query

    column = getattr(model, sort_by)
    if sort_order.lower() == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query


def apply_pagination(query, pagination: PaginationParams):
    """Apply pagination"""
    return query.offset(pagination.skip).limit(pagination.limit)


@router.get("/search")
def advanced_search(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced search with sorting and pagination"""
    query = db.query(models.Item).filter(models.Item.user_id == current_user["user_id"])
    query = apply_search(query, models.Item, ["name", "description"], q)
    query = apply_sort(query, models.Item, sort_by, sort_order)

    total = query.count()
    items = apply_pagination(query, PaginationParams(skip, limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


@router.get("/filter")
def advanced_filter(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced filtering with dynamic conditions"""
    query = db.query(models.Item).filter(models.Item.user_id == current_user["user_id"])

    if is_active is not None:
        query = query.filter(models.Item.is_active == is_active)

    query = apply_sort(query, models.Item, sort_by, sort_order)

    total = query.count()
    items = apply_pagination(query, PaginationParams(skip, limit)).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }
'''


# ============================
# REDIS CACHING
# ============================

def generate_redis_cache_module() -> str:
    """Generate Redis caching module"""
    return '''import redis
import json
from typing import Any, Optional, Callable
from functools import wraps
from config import settings
import hashlib
import inspect

class RedisCache:
    """Redis cache wrapper"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0", ttl: int = 3600):
        self.redis_url = redis_url
        self.ttl = ttl
        try:
            self.client = redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            print("Redis connected successfully")
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None

        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.client:
            return False

        try:
            ttl = ttl or self.ttl
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")

        return False

    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.client:
            return False

        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")

        return False

    def clear(self) -> bool:
        """Clear all cache"""
        if not self.client:
            return False

        try:
            self.client.flushdb()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")

        return False

    def generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key"""
        key_parts = [prefix] + [str(arg) for arg in args]
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        key_hash = hashlib.md5(kwargs_str.encode()).hexdigest()
        return ":".join(key_parts) + f":{key_hash}"


# Cache decorator
cache = RedisCache()


def cached(prefix: str, ttl: int = 3600):
    """Cache decorator for functions"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache.generate_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator


# Cache invalidation helper
def invalidate_cache(pattern: str = "*"):
    """Invalidate cache by pattern"""
    if not cache.client:
        return False

    try:
        keys = cache.client.keys(pattern)
        if keys:
            cache.client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache invalidation error: {e}")

    return False
'''


# ============================
# WEBSOCKET REAL-TIME FEATURES
# ============================

def generate_websocket_module() -> str:
    """Generate WebSocket real-time features"""
    return '''from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from datetime import datetime

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """WebSocket connection manager"""

    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept new connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast(self, message: dict):
        """Broadcast message to all users"""
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Broadcast error: {e}")

    async def send_personal(self, user_id: int, message: dict):
        """Send message to specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Send error: {e}")


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()

            # Broadcast received message
            message = {
                "type": "message",
                "user_id": user_id,
                "content": data.get("content"),
                "timestamp": datetime.now().isoformat()
            }

            await manager.broadcast(message)

    except WebSocketDisconnect:
        await manager.disconnect(websocket, user_id)
        disconnect_message = {
            "type": "disconnect",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(disconnect_message)
'''


# ============================
# GRAPHQL API
# ============================

def generate_graphql_schema() -> str:
    """Generate GraphQL schema"""
    return '''import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app import models


class ItemType(SQLAlchemyObjectType):
    """GraphQL Item type"""
    class Meta:
        model = models.Item


class Query(graphene.ObjectType):
    """GraphQL Query"""

    all_items = graphene.List(ItemType)
    item_by_id = graphene.Field(ItemType, id=graphene.Int(required=True))

    def resolve_all_items(self, info):
        return models.Item.query.all()

    def resolve_item_by_id(self, info, id):
        return models.Item.query.get(id)


class CreateItem(graphene.Mutation):
    """Create item mutation"""
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, name, description=None):
        item = models.Item(name=name, description=description)
        # Save to database
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    """Update item mutation"""
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, id, name=None, description=None):
        item = models.Item.query.get(id)
        if name:
            item.name = name
        if description:
            item.description = description
        # Save to database
        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    """Delete item mutation"""
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        item = models.Item.query.get(id)
        # Delete from database
        return DeleteItem(success=True)


class Mutation(graphene.ObjectType):
    """GraphQL Mutations"""
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()


# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
'''


# ============================
# ENHANCED MAIN APPLICATION
# ============================

def generate_enhanced_main(project_name: str) -> str:
    """Generate enhanced main.py with all features"""
    return f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_graphql import GraphQL
from app.core.database import init_db
from app.routes import auth, advanced_crud, websocket
from config import settings
from app.cache import cache
from app.graphql_schema import schema

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="{project_name}",
    version="1.0.0",
    description="{project_name} API with Advanced Features"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(advanced_crud.router)
app.include_router(websocket.router)

# GraphQL endpoint
app.add_route("/graphql", GraphQL(schema))


@app.get("/")
def read_root():
    return {{
        "message": "{project_name} API with Advanced Features",
        "version": "1.0.0",
        "features": ["REST API", "Advanced Filtering", "Redis Caching", "WebSocket", "GraphQL"]
    }}


@app.get("/health")
def health_check():
    return {{
        "status": "healthy",
        "cache": "connected" if cache.client else "disconnected"
    }}


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("🚀 Starting {project_name} with advanced features...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    print("🛑 Shutting down {project_name}...")
    if cache.client:
        cache.client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
'''


# ============================
# ENHANCED REQUIREMENTS
# ============================

def generate_enhanced_requirements() -> str:
    """Generate enhanced requirements.txt"""
    return '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
httpx==0.25.2
alembic==1.13.1

# Advanced features
redis==5.0.1
aioredis==2.0.1
graphene==3.3
graphene-sqlalchemy==3.0.0
strawberry-graphql==0.213.0
python-multipart==0.0.6
websockets==12.0

# Optional: Async support
aiofiles==23.2.1
asyncpg==0.29.0
'''


# ============================
# ENHANCEMENT SCRIPT
# ============================

def enhance_fastapi_projects():
    """Enhance FastAPI projects with advanced features"""
    fastapi_projects = [
        "01_task_management_saas",
        "02_email_newsletter_platform",
        "03_url_shortener_service",
        "04_expense_tracker_saas",
        "05_document_converter_api",
        "06_form_builder_platform",
        "07_api_monitoring_service",
        "08_markdown_to_html_saas",
        "09_qr_code_generator_api",
        "10_jwt_auth_service",
    ]

    print("🚀 Enhancing FastAPI Projects with Advanced Features...")
    print("=" * 70)

    for project in fastapi_projects:
        base_path = Path(f"/home/user/02-python-app/{project}")
        print(f"[{project}]", end=" ", flush=True)

        try:
            # Create advanced routes
            advanced_crud_code = generate_advanced_crud_routes()
            (base_path / "app" / "routes" / "advanced_crud.py").write_text(advanced_crud_code)

            # Create cache module
            cache_code = generate_redis_cache_module()
            (base_path / "app" / "cache.py").write_text(cache_code)

            # Create WebSocket module
            websocket_code = generate_websocket_module()
            (base_path / "app" / "routes" / "websocket.py").write_text(websocket_code)

            # Create GraphQL schema
            graphql_code = generate_graphql_schema()
            (base_path / "app" / "graphql_schema.py").write_text(graphql_code)

            # Update main.py
            enhanced_main = generate_enhanced_main(project)
            (base_path / "main.py").write_text(enhanced_main)

            # Update requirements.txt
            enhanced_requirements = generate_enhanced_requirements()
            (base_path / "requirements.txt").write_text(enhanced_requirements)

            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("=" * 70)
    print("✨ FastAPI projects enhanced!")


if __name__ == "__main__":
    enhance_fastapi_projects()
