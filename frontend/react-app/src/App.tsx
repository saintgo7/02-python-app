import React, { useState } from 'react';
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
