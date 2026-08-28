import React, { createContext, useContext, useEffect, useState } from 'react';
import { apiClient } from '@/services/api';
import { Organization, Workspace } from '@/types';

interface WorkspaceContextType {
  currentOrg: Organization | null;
  currentWorkspace: Workspace | null;
  organizations: Organization[];
  workspaces: Workspace[];
  switchWorkspace: (workspaceId: string) => void;
  switchOrganization: (orgId: string) => void;
  refreshWorkspaces: () => Promise<void>;
}

const WorkspaceContext = createContext<WorkspaceContextType | undefined>(undefined);

export const WorkspaceProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [currentOrg, setCurrentOrg] = useState<Organization | null>(null);
  const [currentWorkspace, setCurrentWorkspace] = useState<Workspace | null>(null);

  const refreshWorkspaces = async () => {
    try {
      const orgRes = await apiClient.get('/organizations');
      const orgList = orgRes.data.items || [];
      setOrganizations(orgList);

      if (orgList.length > 0) {
        const savedOrgId = localStorage.getItem('dfx_active_org_id');
        const activeOrg = orgList.find((o: Organization) => o.id === savedOrgId) || orgList[0];
        setCurrentOrg(activeOrg);
        localStorage.setItem('dfx_active_org_id', activeOrg.id);

        const wsRes = await apiClient.get(`/organizations/${activeOrg.id}/workspaces`);
        const wsList = wsRes.data || [];
        setWorkspaces(wsList);

        if (wsList.length > 0) {
          const savedWsId = localStorage.getItem('dfx_active_workspace_id');
          const activeWs = wsList.find((w: Workspace) => w.id === savedWsId) || wsList[0];
          setCurrentWorkspace(activeWs);
          localStorage.setItem('dfx_active_workspace_id', activeWs.id);
        }
      }
    } catch (err) {
      console.error('Failed to load workspaces:', err);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('dfx_access_token');
    if (token) {
      refreshWorkspaces();
    }
  }, []);

  const switchWorkspace = (workspaceId: string) => {
    const ws = workspaces.find((w) => w.id === workspaceId);
    if (ws) {
      setCurrentWorkspace(ws);
      localStorage.setItem('dfx_active_workspace_id', ws.id);
      window.location.reload();
    }
  };

  const switchOrganization = (orgId: string) => {
    const org = organizations.find((o) => o.id === orgId);
    if (org) {
      setCurrentOrg(org);
      localStorage.setItem('dfx_active_org_id', org.id);
      refreshWorkspaces();
    }
  };

  return (
    <WorkspaceContext.Provider
      value={{
        currentOrg,
        currentWorkspace,
        organizations,
        workspaces,
        switchWorkspace,
        switchOrganization,
        refreshWorkspaces,
      }}
    >
      {children}
    </WorkspaceContext.Provider>
  );
};

export const useWorkspace = () => {
  const context = useContext(WorkspaceContext);
  if (!context) {
    throw new Error('useWorkspace must be used within a WorkspaceProvider');
  }
  return context;
};
