// User Types
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
