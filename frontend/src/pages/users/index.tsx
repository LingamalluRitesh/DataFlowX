import React, { useEffect, useState } from 'react';
import { Key, Plus, Shield, User, Users } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export default function UsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchUsersData = async () => {
    setLoading(true);
    try {
      const [usersRes, rolesRes] = await Promise.all([
        apiClient.get('/users'),
        apiClient.get('/users/roles'),
      ]);
      setUsers(usersRes.data.items || []);
      setRoles(rolesRes.data || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsersData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Team & Role-Based Access Control (RBAC)</h1>
          <p className="text-sm text-slate-400 mt-1">Manage organization members, service accounts, and permissions</p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Organization Members</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-6">User</th>
                <th className="py-3 px-6">Email</th>
                <th className="py-3 px-6">Role</th>
                <th className="py-3 px-6">Status</th>
                <th className="py-3 px-6">Joined Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-6 font-semibold text-slate-100 flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xs">
                      {u.full_name?.charAt(0) || u.email.charAt(0).toUpperCase()}
                    </div>
                    <span>{u.full_name || u.username}</span>
                  </td>
                  <td className="py-3.5 px-6 text-slate-400 font-mono">{u.email}</td>
                  <td className="py-3.5 px-6">
                    <Badge variant={u.is_superuser ? 'primary' : 'neutral'}>
                      {u.is_superuser ? 'SUPER ADMIN' : 'DATA ENGINEER'}
                    </Badge>
                  </td>
                  <td className="py-3.5 px-6">
                    <Badge variant={u.is_active ? 'success' : 'danger'}>
                      {u.is_active ? 'ACTIVE' : 'DISABLED'}
                    </Badge>
                  </td>
                  <td className="py-3.5 px-6 text-slate-400">{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
