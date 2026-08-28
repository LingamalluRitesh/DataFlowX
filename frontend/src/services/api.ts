import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to attach JWT token and Workspace ID
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('dfx_access_token');
    const workspaceId = localStorage.getItem('dfx_active_workspace_id');
    const orgId = localStorage.getItem('dfx_active_org_id');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    if (workspaceId) {
      config.headers['X-Workspace-ID'] = workspaceId;
    }
    if (orgId) {
      config.headers['X-Organization-ID'] = orgId;
    }
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      const refreshToken = localStorage.getItem('dfx_refresh_token');
      if (refreshToken && !error.config._retry) {
        error.config._retry = true;
        try {
          const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          localStorage.setItem('dfx_access_token', res.data.access_token);
          localStorage.setItem('dfx_refresh_token', res.data.refresh_token);
          error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
          return apiClient(error.config);
        } catch (refreshErr) {
          localStorage.removeItem('dfx_access_token');
          localStorage.removeItem('dfx_refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
