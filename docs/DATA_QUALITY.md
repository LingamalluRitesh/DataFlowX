# DataFlowX Data Quality & Governance Engine

## 1. Quality Rule Types
DataFlowX provides built-in and extensible validation rules:

1. **`NotNullRule`**: Checks for null, None, or empty string values in mandatory fields.
2. **`UniqueRule`**: Ensures primary key uniqueness across single or multi-column subsets.
3. **`RangeRule`**: Validates numeric metrics within specified `[min_value, max_value]` bounds.
4. **`RegexRule`**: Validates text formats against POSIX regular expressions (e.g., postal codes, phone numbers).
5. **`EmailRule`**: Verifies RFC 5322 compliant email formatting.
6. **`AllowedValuesRule`**: Validates categorical status against fixed enumerated allowlists.
7. **`CustomSqlRule`**: Runs custom boolean SQL assertions against in-flight data.
8. **`DataTypeRule`**: Enforces schema type conformance.

## 2. Failure Actions & Automated Quarantining
When data quality checks detect anomalies, the engine handles records according to the configured failure action:
- **`FAIL_PIPELINE`**: Halts DAG execution immediately and triggers incident notification.
- **`WARN_AND_CONTINUE`**: Logs quality warnings, increments anomaly metrics, and permits data flow.
- **`QUARANTINE_RECORDS`**: Isolates failing records into partitioned Quarantine Parquet storage (`storage/quarantine/{dataset}/{date}/{exec_id}.parquet`), passes valid records downstream, and computes a composite quality score.
