# DataFlowX Orchestration Engine Manual

## 1. Topological Sorting & Cycle Detection
DataFlowX utilizes Kahn's algorithm for Directed Acyclic Graph (DAG) validation:
- Validates node references and endpoint connections.
- Detects circular dependency cycles prior to execution kickoff.
- Partitions the DAG into topological execution layers, running independent upstream tasks concurrently across thread and worker pools.

## 2. Exponential Backoff with Randomized Jitter
The self-healing retry engine prevents thundering herd problems when interacting with third-party rate-limited APIs:
$$\text{Delay}(n) = \min\left(\text{base\_delay} \times \text{multiplier}^{n-1},\, \text{max\_delay}\right)$$
When jitter is enabled, a uniform random variation in the interval $[0, \text{Delay}(n)]$ is applied to ensure desynchronized worker retries.

## 3. Distributed Redlock Scheduler
The scheduler daemon uses Redis Redlock distributed mutual exclusion to guarantee that exactly one scheduler instance triggers a scheduled cron or watermark pipeline at any given moment, preventing duplicate executions in active-active cluster deployments.
