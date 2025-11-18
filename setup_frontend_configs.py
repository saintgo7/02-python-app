#!/usr/bin/env python3
"""
Frontend Configuration Setup
Creates build configs, TypeScript definitions, and environment files
"""

from pathlib import Path

def generate_tsconfig() -> str:
    """Generate TypeScript configuration"""
    return '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "exclude": ["dist", "node_modules"]
}
'''

def generate_vite_config() -> str:
    """Generate Vite configuration"""
    return '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [vue(), react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, ''),
      },
    },
  },
  build: {
    target: 'esnext',
    minify: 'terser',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          react: ['react', 'react-dom', 'react-router-dom'],
        },
      },
    },
  },
})
'''

def generate_env_example() -> str:
    """Generate .env.example file"""
    return '''# API Configuration
REACT_APP_API_URL=http://localhost:8000
VUE_APP_API_URL=http://localhost:8000

# App Configuration
REACT_APP_APP_NAME="Python App"
VUE_APP_APP_NAME="Python App"

# Features
REACT_APP_ENABLE_ANALYTICS=false
VUE_APP_ENABLE_ANALYTICS=false

# Build
BUILD_PATH=./dist
'''

def generate_docker_frontend() -> str:
    """Generate Docker configuration for frontend"""
    return '''FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
'''

def generate_api_types() -> str:
    """Generate TypeScript API types"""
    return '''// User Types
export interface User {
  id: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  id: string;
  email: string;
}

// Item Types
export interface Item {
  id: number;
  name: string;
  description?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateItemRequest {
  name: string;
  description?: string;
}

export interface UpdateItemRequest {
  name?: string;
  description?: string;
}

// Pagination Types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// Error Types
export interface ApiError {
  detail: string;
  status_code: number;
}

// Health Check
export interface HealthResponse {
  status: string;
  version: string;
}
'''

def generate_eslint_config() -> str:
    """Generate ESLint configuration"""
    return '''{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": [
    "react",
    "@typescript-eslint",
    "react-hooks"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react-hooks/rules-of-hooks": "error",
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        "argsIgnorePattern": "^_"
      }
    ]
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
'''

def generate_prettier_config() -> str:
    """Generate Prettier configuration"""
    return '''{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "bracketSpacing": true,
  "endOfLine": "lf"
}
'''

def generate_frontend_readme() -> str:
    """Generate Frontend README"""
    return '''# Frontend Applications

This directory contains modern web frontends for the Python applications.

## Overview

- **React.js**: Frontend for FastAPI projects (01-10)
- **Vue.js**: Frontend for Django projects (11-20)

## Technology Stack

### React.js Frontend
- React 18
- TypeScript
- React Router for navigation
- Zustand for state management
- Axios for API calls
- Tailwind CSS for styling
- React Query for data fetching
- React Hot Toast for notifications

### Vue.js Frontend
- Vue 3
- TypeScript
- Vue Router for navigation
- Pinia for state management
- Axios for API calls
- Vite for bundling
- Tailwind CSS for styling

## Getting Started

### React Frontend

```bash
cd frontend/react-app
npm install
npm start
```

### Vue Frontend

```bash
cd frontend/vue-app
npm install
npm run dev
```

## Project Structure

### React App

```
react-app/
├── src/
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── ItemsPage.tsx
│   ├── stores/
│   │   └── authStore.ts
│   ├── api/
│   │   └── client.ts
│   ├── types/
│   │   └── api.ts
│   ├── App.tsx
│   └── App.css
├── package.json
├── tsconfig.json
└── Dockerfile
```

### Vue App

```
vue-app/
├── src/
│   ├── pages/
│   ├── stores/
│   ├── components/
│   ├── api/
│   ├── types/
│   └── App.vue
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

## Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Configure API endpoints:

```
REACT_APP_API_URL=http://localhost:8000
VUE_APP_API_URL=http://localhost:8000
```

## API Integration

### Authentication Flow

1. User submits email and password
2. Frontend sends request to `/auth/login` or `/auth/register`
3. Backend returns JWT token
4. Frontend stores token in localStorage
5. All subsequent requests include token in Authorization header

### API Client Configuration

The Axios client automatically:
- Adds JWT token to request headers
- Handles 401 responses by redirecting to login
- Converts responses to JSON
- Includes proper error handling

## Building for Production

### React

```bash
cd frontend/react-app
npm run build
```

### Vue

```bash
cd frontend/vue-app
npm run build
```

## Docker Deployment

### Build Image

```bash
docker build -t python-app-frontend .
```

### Run Container

```bash
docker run -p 3000:3000 python-app-frontend
```

## Testing

### React

```bash
npm test
```

### Vue

```bash
npm run test
```

## Code Quality

### Linting

```bash
npm run lint
```

### Type Checking

```bash
npm run type-check
```

### Formatting

```bash
npx prettier --write src/
```

## Features

### Authentication
- Login page
- Sign-up functionality
- JWT token management
- Automatic logout on 401

### Dashboard
- Welcome message
- Statistics cards
- Recent activity feed
- Real-time updates

### Items Management
- List items with pagination
- Create new items
- Delete items
- Search and filter

### Responsive Design
- Mobile-friendly layout
- Tablet optimized
- Desktop optimized
- Touch-friendly buttons

## Performance Optimizations

- Code splitting with route-based chunks
- Lazy loading components
- Image optimization
- Caching with React Query
- Minified production builds

## Security

- HTTPS ready
- JWT token storage
- XSS protection
- CSRF protection via backend
- Secure headers via backend

## Troubleshooting

### API Connection Issues

1. Check backend is running on correct port
2. Verify CORS is configured correctly
3. Check API_URL environment variable
4. Check network tab in browser dev tools

### Token Issues

1. Clear localStorage
2. Re-login
3. Check token format in Authorization header
4. Verify token is not expired

### Build Issues

1. Clear node_modules: `rm -rf node_modules`
2. Reinstall: `npm install`
3. Clear cache: `npm cache clean --force`
4. Try again: `npm run build`

## Additional Resources

- [React Documentation](https://react.dev)
- [Vue Documentation](https://vuejs.org)
- [TypeScript Documentation](https://www.typescriptlang.org)
- [Axios Documentation](https://axios-http.com)
- [REST API Best Practices](https://restfulapi.net)

## License

MIT
'''

def setup_frontend_configs():
    """Setup frontend configurations"""
    print("⚙️  Setting up Frontend Configurations...")
    print("=" * 70)

    frontend_dir = Path("/home/user/02-python-app/frontend")

    # React configs
    react_dir = frontend_dir / "react-app"
    (react_dir / "tsconfig.json").write_text(generate_tsconfig())
    (react_dir / ".env.example").write_text(generate_env_example())
    (react_dir / "Dockerfile").write_text(generate_docker_frontend())
    (react_dir / ".eslintrc.json").write_text(generate_eslint_config())
    (react_dir / ".prettierrc").write_text(generate_prettier_config())
    (react_dir / "src" / "types").mkdir(exist_ok=True)
    (react_dir / "src" / "types" / "api.ts").write_text(generate_api_types())

    print("[React Configuration]", end=" ", flush=True)
    print("✅")

    # Vue configs
    vue_dir = frontend_dir / "vue-app"
    (vue_dir / "tsconfig.json").write_text(generate_tsconfig())
    (vue_dir / "vite.config.ts").write_text(generate_vite_config())
    (vue_dir / ".env.example").write_text(generate_env_example())
    (vue_dir / "Dockerfile").write_text(generate_docker_frontend())
    (vue_dir / ".eslintrc.json").write_text(generate_eslint_config())
    (vue_dir / ".prettierrc").write_text(generate_prettier_config())
    (vue_dir / "src" / "types").mkdir(exist_ok=True)
    (vue_dir / "src" / "types" / "api.ts").write_text(generate_api_types())

    print("[Vue Configuration]", end=" ", flush=True)
    print("✅")

    # Root README
    (frontend_dir / "README.md").write_text(generate_frontend_readme())
    print("[Documentation]", end=" ", flush=True)
    print("✅")

    print("=" * 70)
    print("✨ Frontend configuration setup complete!")
    print("\nConfiguration Summary:")
    print(f"  ✓ TypeScript configurations")
    print(f"  ✓ Vite build configuration")
    print(f"  ✓ ESLint and Prettier configs")
    print(f"  ✓ Docker configurations")
    print(f"  ✓ Environment variables")
    print(f"  ✓ API type definitions")
    print(f"  ✓ Comprehensive README")


if __name__ == "__main__":
    setup_frontend_configs()
