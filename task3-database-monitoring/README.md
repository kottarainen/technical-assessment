# # Task 3: Database Performance Analysis

## Scenario

A major e-commerce platform is experiencing intermittent performance issues in PostgreSQL during peak hours. The goal is to create a monitoring script can identify bottlenecks and provide recommendations for optimization.

---

## Features

The script collects and displays key performance metrics from the PostgreSQL RDS instance:

### System Resources
- Cache hit ratio (used as a proxy for CPU/memory usage on managed RDS, where OS level metrics are restricted)


### Connection Management
- Number of active connections
- Number of active transactions

### Query Performance
- Count of slow queries (avg execution time > 200ms)
- Top 10 slowest queries based on average execution time  
*(uses `pg_stat_statements`)*

### Storage Usage
- Total database size
- Top 5 largest tables

---
## Note
- The credentials in `config.py` are placeholders. In real-world scenarios, environment variables or secret managers (e.g., AWS Secrets Manager) should be used instead.
- Make sure `pg_stat_statements` is enabled on your PostgreSQL RDS instance. It can be enabled by modifying the RDS parameter group (`shared_preload_libraries = 'pg_stat_statements'`).

##  Structure

```bash
task3-database-monitoring/
├── db_monitor.py       # Main monitoring script
├── config.py           # PostgreSQL DB connection settings (placeholder credentials)
├── requirements.txt    
└── .gitignore          

