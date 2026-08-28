import React from 'react';
import { Bell, ChevronDown, LogOut, Search, User as UserIcon } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useWorkspace } from '@/context/WorkspaceContext';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { currentOrg, currentWorkspace, organizations, workspaces, switchWorkspace, switchOrganization } = useWorkspace();

  return (
    <header className="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-6 z-10">
      {/* Workspace / Org Switcher & Global Search */}
      <div className="flex items-center gap-4">
        {/* Workspace Dropdown */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <div className="w-2 h-2 rounded-full bg-blue-500" />
          <select
            value={currentWorkspace?.id || ''}
            onChange={(e) => switchWorkspace(e.target.value)}
            aria-label="Active workspace selection"
            className="bg-transparent text-xs font-semibold text-slate-800 dark:text-slate-200 focus:outline-none cursor-pointer"
          >
            {workspaces.map((w) => (
              <option key={w.id} value={w.id} className="dark:bg-slate-900 text-slate-800 dark:text-slate-200">
                {w.name}
              </option>
            ))}
          </select>
        </div>

        {/* Search Bar */}
        <div className="relative w-64">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search pipelines, datasets, sources..."
            className="w-full pl-9 pr-4 py-1.5 text-xs bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 text-slate-800 dark:text-slate-200"
          />
        </div>
      </div>

      {/* User Actions & Profile */}
      <div className="flex items-center gap-4">
        {/* Notification Bell */}
        <button
          aria-label="View system notifications"
          className="relative p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-3 border-l border-slate-200 dark:border-slate-800">
          <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-600 dark:text-blue-300 flex items-center justify-center font-bold text-xs">
            {user?.full_name?.charAt(0) || user?.email?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="hidden md:block text-left">
            <p className="text-xs font-semibold text-slate-900 dark:text-slate-100">{user?.full_name || user?.username}</p>
            <p className="text-[11px] text-slate-400">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            className="p-2 text-slate-400 hover:text-red-500 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Logout"
            aria-label="Sign out of your account"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
