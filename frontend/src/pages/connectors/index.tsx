import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { NewSourceModal } from '@/components/modals/NewSourceModal';
import { Database, Plus, CheckCircle, Zap, Search, Server, Cloud, Layers } from 'lucide-react';

interface ConnectorCardItem {
  id: string;
  name: string;
  category: 'RDBMS' | 'WAREHOUSE' | 'STREAMING' | 'SAAS' | 'OBJECT_STORE' | 'NOSQL' | 'ANALYTICAL';
  protocol: string;
  status: 'CONNECTED' | 'AVAILABLE';
  version: string;
}

const allConnectors: ConnectorCardItem[] = [
  { id: 'postgres', name: 'PostgreSQL', category: 'RDBMS', protocol: 'PGWire v3.0', status: 'CONNECTED', version: '16.2' },
  { id: 'mysql', name: 'MySQL', category: 'RDBMS', protocol: 'MySQL Binary', status: 'CONNECTED', version: '8.0' },
  { id: 'snowflake', name: 'Snowflake', category: 'WAREHOUSE', protocol: 'Snowflake REST', status: 'CONNECTED', version: 'Enterprise' },
  { id: 'bigquery', name: 'Google BigQuery', category: 'WAREHOUSE', protocol: 'BigQuery Storage API', status: 'CONNECTED', version: 'v2' },
  { id: 'redshift', name: 'Amazon Redshift', category: 'WAREHOUSE', protocol: 'Redshift Data API', status: 'CONNECTED', version: 'Serverless' },
  { id: 'kafka', name: 'Apache Kafka', category: 'STREAMING', protocol: 'Kafka Binary Wire', status: 'CONNECTED', version: '3.7' },
  { id: 'redis_stream', name: 'Redis Streams', category: 'STREAMING', protocol: 'RESP v3', status: 'CONNECTED', version: '7.2' },
  { id: 'grpc', name: 'gRPC High-Speed', category: 'STREAMING', protocol: 'HTTP/2 Protobuf', status: 'CONNECTED', version: 'v1.60' },
  { id: 's3', name: 'Amazon S3', category: 'OBJECT_STORE', protocol: 'S3 REST SigV4', status: 'CONNECTED', version: 'AWS SDK' },
  { id: 'minio', name: 'MinIO Lake', category: 'OBJECT_STORE', protocol: 'S3 REST SigV4', status: 'CONNECTED', version: 'RELEASE' },
  { id: 'azure_blob', name: 'Azure Blob / ADLS', category: 'OBJECT_STORE', protocol: 'Azure Data Lake REST', status: 'CONNECTED', version: '2023-11' },
  { id: 'elasticsearch', name: 'Elasticsearch', category: 'NOSQL', protocol: 'Elastic HTTP', status: 'CONNECTED', version: '8.12' },
  { id: 'dynamodb', name: 'Amazon DynamoDB', category: 'NOSQL', protocol: 'DynamoDB JSON', status: 'CONNECTED', version: 'AWS v2' },
  { id: 'cassandra', name: 'Apache Cassandra', category: 'NOSQL', protocol: 'CQL v4', status: 'CONNECTED', version: '4.1' },
  { id: 'clickhouse', name: 'ClickHouse OLAP', category: 'ANALYTICAL', protocol: 'ClickHouse Native/HTTP', status: 'CONNECTED', version: '24.3' },
  { id: 'duckdb', name: 'DuckDB In-Process', category: 'ANALYTICAL', protocol: 'C++ Native', status: 'CONNECTED', version: '0.10.0' },
  { id: 'neo4j', name: 'Neo4j Graph', category: 'NOSQL', protocol: 'Bolt v5', status: 'CONNECTED', version: '5.18' },
  { id: 'salesforce', name: 'Salesforce CRM', category: 'SAAS', protocol: 'Salesforce REST / Bulk v2', status: 'CONNECTED', version: 'v59.0' },
  { id: 'hubspot', name: 'HubSpot Marketing', category: 'SAAS', protocol: 'HubSpot CRM v3', status: 'CONNECTED', version: 'v3' },
  { id: 'stripe', name: 'Stripe Billing', category: 'SAAS', protocol: 'Stripe Events API', status: 'CONNECTED', version: '2023-10' },
  { id: 'servicenow', name: 'ServiceNow ITSM', category: 'SAAS', protocol: 'Table API', status: 'CONNECTED', version: 'Washington' },
  { id: 'jira', name: 'Atlassian Jira', category: 'SAAS', protocol: 'Jira Cloud REST v3', status: 'CONNECTED', version: 'v3' },
  { id: 'zendesk', name: 'Zendesk Support', category: 'SAAS', protocol: 'Zendesk Incremental v2', status: 'CONNECTED', version: 'v2' },
  { id: 'oracle', name: 'Oracle Database', category: 'RDBMS', protocol: 'Oracle TNS / OCI', status: 'CONNECTED', version: '19c/21c' },
  { id: 'sqlserver', name: 'Microsoft SQL Server', category: 'RDBMS', protocol: 'TDS 7.4', status: 'CONNECTED', version: '2022' },
  { id: 'teradata', name: 'Teradata Vantage', category: 'WAREHOUSE', protocol: 'FastExport CLI', status: 'CONNECTED', version: '17.20' },
  { id: 'sap_hana', name: 'SAP HANA ERP', category: 'WAREHOUSE', protocol: 'HDB SQL', status: 'CONNECTED', version: '2.0 SPS07' },
  { id: 'google_sheets', name: 'Google Sheets', category: 'SAAS', protocol: 'Sheets API v4', status: 'CONNECTED', version: 'v4' },
];

export default function ConnectorsHubPage() {
  const [filterCat, setFilterCat] = useState<string>('ALL');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const filtered = filterCat === 'ALL' ? allConnectors : allConnectors.filter((c) => c.category === filterCat);

  const columns: DataGridColumn<ConnectorCardItem>[] = [
    {
      key: 'name',
      header: 'Connector Integration',
      render: (c) => (
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-cyan-400">
            {c.name.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <strong className="text-white text-sm">{c.name}</strong>
            <div className="text-[10px] text-slate-500 font-mono">{c.protocol}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Category',
      render: (c) => (
        <span className="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">
          {c.category}
        </span>
      ),
    },
    { key: 'version', header: 'Supported Engine Version', render: (c) => <span className="font-mono text-xs text-slate-400">{c.version}</span> },
    {
      key: 'status',
      header: 'Driver Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold flex items-center gap-1 w-max">
          <CheckCircle className="w-3 h-3" /> {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Connectors Hub & Heterogeneous Data Sources — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Database className="w-7 h-7 text-cyan-400" />
              Heterogeneous Connectors Hub (28+ Connectors)
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Connect to enterprise databases, cloud data warehouses, real-time message streams, object stores, and SaaS applications.
            </p>
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto"
          >
            <Plus className="w-4 h-4" /> Add Connection
          </button>
        </div>

        {/* Filter Buttons */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {['ALL', 'WAREHOUSE', 'RDBMS', 'STREAMING', 'OBJECT_STORE', 'NOSQL', 'ANALYTICAL', 'SAAS'].map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCat(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                filterCat === cat
                  ? 'bg-cyan-600 text-white font-semibold'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <DataGrid data={filtered} columns={columns} title="Registered Connectors Catalog" />

        <NewSourceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      </div>
    </MainLayout>
  );
}
