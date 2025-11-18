import React from 'react';
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
