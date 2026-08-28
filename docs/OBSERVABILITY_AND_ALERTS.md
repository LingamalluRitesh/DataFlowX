# DataFlowX Observability & Monitoring Manual

## 1. Prometheus Metric Exposition
DataFlowX exposes industry-standard Prometheus metrics at `GET /metrics`:
- `dfx_pipeline_executions_total{pipeline_id, status}`: Counter of pipeline runs.
- `dfx_pipeline_duration_seconds{pipeline_id}`: Histogram of run durations.
- `dfx_records_processed_total{pipeline_id, layer}`: Counter of processed records.
- `dfx_records_quarantined_total{pipeline_id, rule}`: Counter of quarantined bad rows.
- `dfx_data_quality_score{pipeline_id}`: Gauge of overall data quality percentage.
- `dfx_worker_cpu_percent{worker_id}`: Worker CPU utilization.
- `dfx_worker_memory_bytes{worker_id}`: Worker memory footprint.

## 2. Real-Time Alert Engine
- **SLA Breach Alerts**: Triggers when a pipeline run exceeds maximum threshold duration.
- **Data Quality Alerts**: Triggers when quality score falls below specified SLA percentage (e.g., < 95%).
- **Consecutive Failure Alerts**: Dispatches incidents when 3 consecutive runs fail.
- **Notification Channels**: Multi-channel dispatching to Slack Webhooks, Microsoft Teams, PagerDuty, and SMTP Email.
