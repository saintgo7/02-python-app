# Frontend Applications

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
