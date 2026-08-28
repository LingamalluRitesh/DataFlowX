# DataFlowX Data Engine Manual

## 1. High-Performance Vectorized Operators
DataFlowX provides vectorized data processing operators built on Pandas and PyArrow C-extensions:
- **`SelectColumnsOperator`**: Restricts projection to designated schema columns.
- **`RenameColumnsOperator`**: Renames attributes according to data dictionary maps.
- **`DropColumnsOperator`**: Removes transient or PII columns.
- **`CastColumnsOperator`**: Casts values into target integer, float, string, or datetime formats.
- **`FilterRowsOperator`**: Vectorized predicate filtering using Python AST expressions.
- **`DeduplicateOperator`**: Removes redundant duplicate records based on primary key combinations.
- **`NormalizeStringsOperator`**: Trims whitespace, cleans ASCII strings, and standardizes case formats (UPPER, LOWER, Title).
- **`FillMissingValuesOperator`**: Imputes null entries using constants, mean, median, or forward/backward fill.
- **`CalculatedColumnOperator`**: Generates computed business metrics across numeric and categorical fields.
- **`AggregateOperator`**: High-performance grouping and rollup aggregations (`sum`, `mean`, `count`, `min`, `max`).
- **`JoinDataFramesOperator`**: Joins datasets using `inner`, `left`, `right`, and `outer` merge semantics.

## 2. In-Memory SQL Transformation
DataFlowX integrates embedded DuckDB and SQLite analytical SQL engines. SQL operators can query in-flight DataFrames directly using ANSI SQL:
```sql
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(order_amount) AS total_revenue,
    AVG(order_amount) AS average_order_value
FROM input_df
WHERE status = 'COMPLETED'
GROUP BY customer_id
ORDER BY total_revenue DESC;
```

## 3. Safe Python Sandbox
For complex custom procedural transformations, DataFlowX includes an AST-verified execution sandbox that restricts forbidden imports (`os`, `sys`, `subprocess`, `socket`) while allowing NumPy and Pandas transformations.
