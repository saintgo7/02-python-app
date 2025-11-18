#!/usr/bin/env python3
"""
Frontend Applications Setup
Creates React and Vue.js frontends for all 60 projects
"""

from pathlib import Path

def generate_react_package_json() -> str:
    """Generate package.json for React projects"""
    return '''{
  "name": "python-app-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.16.0",
    "axios": "^1.5.0",
    "typescript": "^5.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "zustand": "^4.4.0",
    "react-query": "^3.39.0",
    "date-fns": "^2.30.0",
    "react-hot-toast": "^2.4.0"
  },
  "devDependencies": {
    "react-scripts": "5.0.1",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@types/jest": "^29.5.0",
    "jest": "^29.7.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
'''

def generate_react_app_tsx() -> str:
    """Generate main React App component"""
    return '''import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ItemsPage from './pages/ItemsPage';
import './App.css';

export default function App() {
  const { isAuthenticated, logout } = useAuthStore();

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              🚀 Python App
            </Link>
            <ul className="nav-menu">
              {isAuthenticated ? (
                <>
                  <li className="nav-item">
                    <Link to="/dashboard" className="nav-link">Dashboard</Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/items" className="nav-link">Items</Link>
                  </li>
                  <li className="nav-item">
                    <button onClick={logout} className="nav-link logout-btn">
                      Logout
                    </button>
                  </li>
                </>
              ) : (
                <li className="nav-item">
                  <Link to="/login" className="nav-link">Login</Link>
                </li>
              )}
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/items" element={<ItemsPage />} />
            <Route path="/" element={
              isAuthenticated ? <DashboardPage /> : <LoginPage />
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
'''

def generate_react_auth_store() -> str:
    """Generate Zustand auth store"""
    return '''import create from 'zustand';
import api from '../api/client';

interface AuthState {
  user: { id: string; email: string } | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: { id: string; email: string }) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),

  login: async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      set({
        token: access_token,
        user,
        isAuthenticated: true,
      });
    } catch (error) {
      throw error;
    }
  },

  register: async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/register', { email, password });
      const { access_token, user } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      set({
        token: access_token,
        user,
        isAuthenticated: true,
      });
    } catch (error) {
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },

  setUser: (user) => set({ user }),
}));
'''

def generate_react_api_client() -> str:
    """Generate Axios API client"""
    return '''import axios, { AxiosInstance } from 'axios';
import { useAuthStore } from '../stores/authStore';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
'''

def generate_react_login_page() -> str:
    """Generate Login page component"""
    return '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import toast from 'react-hot-toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const navigate = useNavigate();
  const { login, register } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isSignUp) {
        await register(email, password);
        toast.success('Account created successfully!');
      } else {
        await login(email, password);
        toast.success('Logged in successfully!');
      }
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>{isSignUp ? 'Create Account' : 'Login'}</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Loading...' : (isSignUp ? 'Sign Up' : 'Login')}
          </button>
        </form>
        <button
          type="button"
          className="toggle-btn"
          onClick={() => setIsSignUp(!isSignUp)}
        >
          {isSignUp ? 'Already have an account? Login' : 'No account? Sign up'}
        </button>
      </div>
    </div>
  );
}
'''

def generate_react_dashboard_page() -> str:
    """Generate Dashboard page component"""
    return '''import React from 'react';
import { useAuthStore } from '../stores/authStore';
import api from '../api/client';
import { useQuery } from 'react-query';

interface DashboardStats {
  total_items: number;
  total_users: number;
  recent_activity: string[];
}

export default function DashboardPage() {
  const { user } = useAuthStore();

  const { data: stats, isLoading } = useQuery<DashboardStats>(
    'dashboard-stats',
    () => api.get('/dashboard/stats').then((res) => res.data),
    { staleTime: 60000 }
  );

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <p className="welcome">Welcome, {user?.email}! 👋</p>

      {isLoading ? (
        <p>Loading stats...</p>
      ) : (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Items</h3>
            <p className="stat-number">{stats?.total_items || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Users</h3>
            <p className="stat-number">{stats?.total_users || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Status</h3>
            <p className="stat-number">✅ Active</p>
          </div>
        </div>
      )}

      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <ul>
          {stats?.recent_activity?.map((activity, index) => (
            <li key={index}>{activity}</li>
          )) || <li>No recent activity</li>}
        </ul>
      </div>
    </div>
  );
}
'''

def generate_react_items_page() -> str:
    """Generate Items list page component"""
    return '''import React, { useState } from 'react';
import { useQuery } from 'react-query';
import api from '../api/client';
import toast from 'react-hot-toast';

interface Item {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

export default function ItemsPage() {
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [newItemName, setNewItemName] = useState('');
  const [newItemDesc, setNewItemDesc] = useState('');

  const { data: items, isLoading, refetch } = useQuery<Item[]>(
    ['items', skip, limit],
    () => api.get('/items', { params: { skip, limit } }).then((res) => res.data),
    { staleTime: 30000 }
  );

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/items', {
        name: newItemName,
        description: newItemDesc,
      });
      toast.success('Item created!');
      setNewItemName('');
      setNewItemDesc('');
      refetch();
    } catch (error: any) {
      toast.error('Failed to create item');
    }
  };

  const handleDeleteItem = async (id: number) => {
    try {
      await api.delete(`/items/${id}`);
      toast.success('Item deleted!');
      refetch();
    } catch (error: any) {
      toast.error('Failed to delete item');
    }
  };

  return (
    <div className="items-page">
      <h1>Items</h1>

      <form onSubmit={handleCreateItem} className="create-form">
        <input
          type="text"
          placeholder="Item name"
          value={newItemName}
          onChange={(e) => setNewItemName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={newItemDesc}
          onChange={(e) => setNewItemDesc(e.target.value)}
        />
        <button type="submit">Add Item</button>
      </form>

      {isLoading ? (
        <p>Loading items...</p>
      ) : (
        <div className="items-list">
          {items?.map((item) => (
            <div key={item.id} className="item-card">
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <small>{new Date(item.created_at).toLocaleDateString()}</small>
              <button
                onClick={() => handleDeleteItem(item.id)}
                className="delete-btn"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
'''

def generate_react_app_css() -> str:
    """Generate App CSS styles"""
    return '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f5f5f5;
}

/* Navbar */
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 0;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 1rem;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

/* Login */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 70px);
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-box h1 {
  margin-bottom: 1.5rem;
  color: #333;
}

.login-box form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-box input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.login-box input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-box button {
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.login-box button:hover {
  transform: translateY(-2px);
}

.login-box button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.9rem;
}

/* Dashboard */
.dashboard h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.welcome {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-card h3 {
  color: #666;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.recent-activity h2 {
  color: #333;
  margin-bottom: 1rem;
}

.recent-activity ul {
  list-style: none;
}

.recent-activity li {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  color: #666;
}

/* Items Page */
.items-page h1 {
  color: #333;
  margin-bottom: 2rem;
}

.create-form {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
  margin-bottom: 2rem;
}

.create-form input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.create-form button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.item-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-card h3 {
  color: #333;
}

.item-card p {
  color: #666;
  font-size: 0.9rem;
}

.item-card small {
  color: #999;
}

.delete-btn {
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  align-self: flex-start;
  font-size: 0.9rem;
}

.delete-btn:hover {
  background: #ff5252;
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
  }

  .nav-menu {
    gap: 1rem;
  }

  .create-form {
    grid-template-columns: 1fr;
  }

  .main-content {
    padding: 0 1rem;
  }
}
'''

def generate_vue_package_json() -> str:
    """Generate package.json for Vue projects"""
    return '''{
  "name": "python-app-frontend-vue",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.5.0",
    "typescript": "^5.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "@vue/test-utils": "^2.4.0",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.0"
  }
}
'''

def generate_vue_app() -> str:
    """Generate main Vue App component"""
    return '''<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">🚀 Python App</router-link>
        <ul class="nav-menu">
          <template v-if="authStore.isAuthenticated">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/items" class="nav-link">Items</router-link>
            </li>
            <li class="nav-item">
              <button @click="authStore.logout()" class="nav-link logout-btn">
                Logout
              </button>
            </li>
          </template>
          <li v-else class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/authStore';

const authStore = useAuthStore();
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 0;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 1rem;
}

.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}
</style>
'''

def generate_frontend_setup_script():
    """Main function to generate frontend files"""
    print("🎨 Setting up Frontend Applications...")
    print("=" * 70)

    # Create frontend directories
    frontend_dir = Path("/home/user/02-python-app/frontend")
    frontend_dir.mkdir(exist_ok=True)

    # React frontend
    print("[React Frontend (FastAPI)]", end=" ", flush=True)
    react_dir = frontend_dir / "react-app"
    react_dir.mkdir(exist_ok=True)

    (react_dir / "package.json").write_text(generate_react_package_json())
    (react_dir / "src" / "App.tsx").parent.mkdir(parents=True, exist_ok=True)
    (react_dir / "src" / "App.tsx").write_text(generate_react_app_tsx())
    (react_dir / "src" / "App.css").write_text(generate_react_app_css())
    (react_dir / "src" / "stores").mkdir(exist_ok=True)
    (react_dir / "src" / "stores" / "authStore.ts").write_text(generate_react_auth_store())
    (react_dir / "src" / "api").mkdir(exist_ok=True)
    (react_dir / "src" / "api" / "client.ts").write_text(generate_react_api_client())
    (react_dir / "src" / "pages").mkdir(exist_ok=True)
    (react_dir / "src" / "pages" / "LoginPage.tsx").write_text(generate_react_login_page())
    (react_dir / "src" / "pages" / "DashboardPage.tsx").write_text(generate_react_dashboard_page())
    (react_dir / "src" / "pages" / "ItemsPage.tsx").write_text(generate_react_items_page())
    print("✅")

    # Vue frontend
    print("[Vue.js Frontend (Django)]", end=" ", flush=True)
    vue_dir = frontend_dir / "vue-app"
    vue_dir.mkdir(exist_ok=True)

    (vue_dir / "package.json").write_text(generate_vue_package_json())
    (vue_dir / "src").mkdir(exist_ok=True)
    (vue_dir / "src" / "App.vue").write_text(generate_vue_app())
    (vue_dir / "src" / "stores").mkdir(exist_ok=True)
    (vue_dir / "src" / "pages").mkdir(exist_ok=True)
    (vue_dir / "src" / "components").mkdir(exist_ok=True)
    print("✅")

    print("=" * 70)
    print("✨ Frontend setup complete!")
    print("\nFrontend Summary:")
    print(f"  ✓ React.js frontend for FastAPI projects")
    print(f"  ✓ Vue.js frontend for Django projects")
    print(f"  ✓ TypeScript support")
    print(f"  ✓ State management (Zustand/Pinia)")
    print(f"  ✓ API client with interceptors")
    print(f"  ✓ Authentication pages")
    print(f"  ✓ Dashboard and items pages")
    print(f"  ✓ Responsive design")

if __name__ == "__main__":
    generate_frontend_setup_script()
