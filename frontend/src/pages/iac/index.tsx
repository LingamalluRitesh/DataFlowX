import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cloud, Server, Code, CheckCircle, Download, Copy, Terminal } from 'lucide-react';

interface IaCModuleItem {
  id: string;
  name: string;
  provider: 'AWS' | 'GCP' | 'AZURE' | 'KUBERNETES_HELM';
  iac_type: 'TERRAFORM_HCL' | 'HELM_CHART';
  resources_managed: string;
  status: 'PROVISIONED' | 'READY_TO_APPLY';
}

const mockModules: IaCModuleItem[] = [
  { id: 'iac_aws_01', name: 'terraform-aws-lakehouse-prod', provider: 'AWS', iac_type: 'TERRAFORM_HCL', resources_managed: 'S3, Glue Catalog, KMS, EKS Workers', status: 'PROVISIONED' },
  { id: 'iac_gcp_02', name: 'terraform-gcp-lakehouse-analytics', provider: 'GCP', iac_type: 'TERRAFORM_HCL', resources_managed: 'GCS Buckets, BigQuery Datasets, Cloud KMS', status: 'PROVISIONED' },
  { id: 'iac_azure_03', name: 'terraform-azure-adls-lakehouse', provider: 'AZURE', iac_type: 'TERRAFORM_HCL', resources_managed: 'ADLS Gen2, Key Vault, AKS Pool', status: 'READY_TO_APPLY' },
  { id: 'iac_helm_04', name: 'helm-chart-dataflowx-workers', provider: 'KUBERNETES_HELM', iac_type: 'HELM_CHART', resources_managed: 'Worker Pods, HPA, Raft StatefulSet', status: 'PROVISIONED' },
];

export default function InfrastructureAsCodePage() {
  const columns: DataGridColumn<IaCModuleItem>[] = [
    {
      key: 'name',
      header: 'Infrastructure Module',
      render: (m) => (
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{m.name}</strong>
        </div>
      ),
    },
    {
      key: 'provider',
      header: 'Cloud Target',
      render: (m) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{m.provider}</span>,
    },
    { key: 'resources_managed', header: 'Managed Resources', render: (m) => <span className="text-slate-300 text-xs">{m.resources_managed}</span> },
    {
      key: 'status',
      header: 'IaC State',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {m.status}
        </span>
      ),
    },
    {
      key: 'id',
      header: 'Action',
      render: (m) => (
        <button className="flex items-center gap-1 px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          <Download className="w-3 h-3" /> Export HCL
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Infrastructure as Code & Multi-Cloud Terraform — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Cloud className="w-7 h-7 text-cyan-400" />
            Infrastructure as Code (IaC) & Multi-Cloud Terraform Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated Terraform HCL and Kubernetes Helm chart generation for multi-cloud Lakehouse infrastructure provisioning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Managed Cloud Modules</div>
            <div className="text-2xl font-bold text-white mt-1">4 Modules</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cloud Targets</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">AWS, GCP, Azure, K8s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compliance Standard</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">CIS Benchmark v1.4</div>
          </div>
        </div>

        <DataGrid data={mockModules} columns={columns} title="Multi-Cloud Infrastructure Modules" />
      </div>
    </MainLayout>
  );
}
