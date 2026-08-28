import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { apiClient } from '@/services/api';
import { UserSessionInfo } from '@/types';

interface AuthContextType {
  user: UserSessionInfo | null;
  loading: boolean;
  login: (usernameOrEmail: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserSessionInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('dfx_access_token');
      if (token) {
        try {
          const res = await apiClient.get('/auth/me');
          setUser(res.data);
          if (res.data.current_workspace_id) {
            localStorage.setItem('dfx_active_workspace_id', res.data.current_workspace_id);
          }
          if (res.data.current_organization_id) {
            localStorage.setItem('dfx_active_org_id', res.data.current_organization_id);
          }
        } catch (err) {
          localStorage.removeItem('dfx_access_token');
          localStorage.removeItem('dfx_refresh_token');
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (usernameOrEmail: string, password: string) => {
    setLoading(true);
    try {
      const res = await apiClient.post('/auth/login', {
        username_or_email: usernameOrEmail,
        password: password,
      });

      localStorage.setItem('dfx_access_token', res.data.access_token);
      localStorage.setItem('dfx_refresh_token', res.data.refresh_token);
      setUser(res.data.user);

      if (res.data.user.current_workspace_id) {
        localStorage.setItem('dfx_active_workspace_id', res.data.user.current_workspace_id);
      }
      if (res.data.user.current_organization_id) {
        localStorage.setItem('dfx_active_org_id', res.data.user.current_organization_id);
      }

      router.push('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('dfx_access_token');
    localStorage.removeItem('dfx_refresh_token');
    localStorage.removeItem('dfx_active_workspace_id');
    localStorage.removeItem('dfx_active_org_id');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
