export type RoleType = 'super_admin' | 'org_admin' | 'data_engineer' | 'data_analyst' | 'data_scientist' | 'viewer';

export type MedallionLayer = 'bronze' | 'silver' | 'gold';

export type PipelineStatus = 'CREATED' | 'QUEUED' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'RETRYING' | 'CANCELLED' | 'PAUSED' | 'TIMEOUT';

export type TaskStatus = 'PENDING' | 'QUEUED' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'RETRYING' | 'SKIPPED' | 'CANCELLED';

export interface UserSessionInfo {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  is_superuser: boolean;
  is_active: boolean;
  current_organization_id?: string;
  current_workspace_id?: string;
  roles: string[];
  permissions: string[];
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: UserSessionInfo;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  logo_url?: string;
  plan: string;
  is_active: boolean;
  created_at: string;
  workspaces?: Workspace[];
}

export interface Workspace {
  id: string;
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
  is_default: boolean;
  created_at: string;
}

export interface DataSource {
  id: string;
  organization_id?: string;
  workspace_id?: string;
  name: string;
  slug: string;
  connector_type: 'postgres' | 'mysql' | 'mongodb' | 'rest' | 'csv' | 'excel' | 'json' | 'kafka' | 's3' | 'minio';
  description?: string;
  status: string;
  health_status: 'healthy' | 'unhealthy' | 'unknown';
  config: Record<string, any>;
  is_active: boolean;
  last_synced_at?: string;
  last_health_check_at?: string;
  created_at: string;
  updated_at: string;
  has_credentials: boolean;
}

export interface Dataset {
  id: string;
  organization_id?: string;
  workspace_id?: string;
  source_id?: string;
  name: string;
  slug: string;
  description?: string;
  layer: MedallionLayer;
  format: string;
  storage_path: string;
  record_count: number;
  size_bytes: number;
  quality_score?: number;
  partition_keys: string[];
  tags: string[];
  owner_email?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DAGNodeData {
  id: string;
  type: string;
  name: string;
  config: Record<string, any>;
  position: { x: number; y: number };
}

export interface DAGEdgeData {
  id?: string;
  source: string;
  target: string;
  source_handle?: string;
  target_handle?: string;
  condition?: string;
}

export interface PipelineDAG {
  nodes: DAGNodeData[];
  edges: DAGEdgeData[];
  globals: Record<string, any>;
}

export interface Pipeline {
  id: string;
  organization_id?: string;
  workspace_id?: string;
  name: string;
  slug: string;
  description?: string;
  pipeline_type: 'batch' | 'streaming';
  environment: 'development' | 'staging' | 'production';
  tags: string[];
  concurrency_limit: number;
  timeout_seconds: number;
  retry_count: number;
  retry_delay_seconds: number;
  status: string;
  active_version_id?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  active_version?: {
    id: string;
    version_number: number;
    dag_definition: PipelineDAG;
    node_count: number;
    edge_count: number;
  };
}

export interface TaskExecution {
  id: string;
  execution_id: string;
  node_id: string;
  task_type: string;
  name: string;
  status: TaskStatus;
  worker_id?: string;
  start_time?: string;
  end_time?: string;
  duration_seconds?: number;
  attempt_number: number;
  max_retries: number;
  records_in: number;
  records_out: number;
  bytes_processed: number;
  error_message?: string;
  created_at: string;
}

export interface Execution {
  id: string;
  organization_id?: string;
  workspace_id?: string;
  pipeline_id: string;
  pipeline_version_id?: string;
  execution_type: string;
  trigger_source?: string;
  status: PipelineStatus;
  start_time?: string;
  end_time?: string;
  duration_seconds?: number;
  total_records_processed: number;
  total_bytes_processed: number;
  records_failed: number;
  quality_score?: number;
  error_summary?: string;
  parameters: Record<string, any>;
  created_at: string;
  tasks?: TaskExecution[];
}

export interface TaskLog {
  id: string;
  task_execution_id?: string;
  log_level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  message: string;
  metadata_json?: Record<string, any>;
  logged_at: string;
}

export interface SystemOverview {
  total_pipelines: number;
  active_pipelines: number;
  running_executions: number;
  total_executions_24h: number;
  success_rate_24h: number;
  total_records_processed_24h: number;
  avg_pipeline_duration_seconds: number;
  average_data_quality_score: number;
  active_workers_count: number;
  active_alert_incidents_count: number;
  total_sources: number;
  total_datasets: number;
}

export interface LineageNode {
  id: string;
  entity_type: string;
  entity_id: string;
  name: string;
  layer?: string;
  metadata: Record<string, any>;
}

export interface LineageEdge {
  id: string;
  source_node_id: string;
  target_node_id: string;
  transformation_type: string;
  pipeline_id?: string;
  execution_id?: string;
  column_mappings?: Record<string, any>;
}

export interface LineageGraph {
  nodes: LineageNode[];
  edges: LineageEdge[];
}

export interface QualityRule {
  id: string;
  name: string;
  rule_type: string;
  description?: string;
  parameters_schema: Record<string, any>;
  default_severity: string;
  is_builtin: boolean;
}

export interface QualitySuite {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  checks?: any[];
}

export interface AlertIncident {
  id: string;
  alert_rule_id: string;
  execution_id?: string;
  title: string;
  description: string;
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  status: 'TRIGGERED' | 'ACKNOWLEDGED' | 'RESOLVED' | 'SUPPRESSED';
  details: Record<string, any>;
  triggered_at: string;
  resolved_at?: string;
}

export interface AuditLog {
  id: string;
  actor_email?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  ip_address?: string;
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  timestamp: string;
}
