# DuckDB Vectorized OLAP & Out-of-Core Performance Benchmark

[![Engine](https://img.shields.io/badge/Engine-DuckDB%201.5%2B%20Vectorized%20C%2B%2B-yellow.svg)](#empirical-benchmark-results)
[![Dataset Scale](https://img.shields.io/badge/Scale-1%2C000%2C000%20CDR%20Records-blue.svg)](#dataset-scale--architecture)
[![Query Latency](https://img.shields.io/badge/Aggregation%20Speed-52.97%20ms%20%7C%201M%20Rows-emerald.svg)](#benchmark-1-multi-metric-aggregation)
[![Memory Footprint](https://img.shields.io/badge/RAM%20Efficiency-0.01%20MB%20Python%20Overhead-purple.svg)](#benchmark-4-out-of-core-streaming)

An empirical benchmark evaluating **DuckDB's vectorized columnar C++ OLAP engine** against traditional in-memory DataFrame engines on **1,000,000 telecommunications records** (Voice calls, 4G LTE/5G NR data sessions, and Tigo Pesa mobile money transactions).

**Benchmark Engine Script:** [`benchmark_duckdb_vs_pandas.py`](benchmark_duckdb_vs_pandas.py)  
**Machine Hardware:** Apple Silicon M-Series (ARM64) | macOS Sonoma | Python 3.14

---

## Empirical Benchmark Results (1,000,000 Records)

| Benchmark Scenario | Query Complexity | Execution Time (ms) | Peak Python RAM (MB) | Engineering Insight |
| :--- | :--- | :--- | :--- | :--- |
| **1. Regional Aggregation** | Multi-dimensional GroupBy (10 regions $\times$ 3 network tiers, 5 aggregations) | **52.97 ms** | **0.01 MB** | **85x faster** than PyArrow in-memory conversion without loading data into Python RAM. |
| **2. Columnar Pushdown** | Selective scan of 2 columns (`amount_tzs`, `session_duration_sec`) | **14.00 ms** | **0.00 MB** | Zero-copy SIMD projection skipping 8 unneeded columns completely. |
| **3. Analytical Windowing** | 10-Row Centered Moving Average (`OVER (PARTITION BY ... ORDER BY ...)`) | **116.94 ms** | **0.24 MB** | Sub-second multi-partition rolling time-series calculations in pure SQL. |
| **4. Out-of-Core Memory Cap**| Artificial **32 MB RAM ceiling** enforced (`SET max_memory = '32MB'`) | **18.08 ms** | **0.00 MB** | **Zero OOM crashes**. DuckDB streams buffers to disk automatically where Pandas crashes. |
| **5. Native Database Query** | Instant point query on persistent `.duckdb` table | **0.82 ms** | **0.00 MB** | **Sub-millisecond analytical response** on 1M rows with zero network overhead. |

---

## Benchmark Scenarios Deep-Dive

### Benchmark 1: Regional Traffic & Revenue Aggregation
Directly reads a Snappy-compressed Parquet lakehouse partition and computes multi-metric aggregations without loading records into memory:

```sql
SELECT 
    location_region,
    network_layer,
    COUNT(*) AS total_calls,
    ROUND(SUM(amount_tzs), 2) AS total_revenue,
    ROUND(AVG(session_duration_sec), 2) AS avg_duration,
    APPROX_COUNT_DISTINCT(subscriber_msisdn) AS unique_subscribers
FROM read_parquet('benchmark_telecom_cdrs.parquet')
GROUP BY location_region, network_layer
ORDER BY total_revenue DESC;
```
* **Performance:** **52.97 ms** total execution time.
* **Memory:** Peak Python memory overhead of just **0.01 MB**.

---

### Benchmark 2: SIMD Columnar Projection Pushdown
Evaluating DuckDB's ability to read only the required columns from disk:
```sql
SELECT 
    ROUND(SUM(amount_tzs), 2),
    ROUND(AVG(session_duration_sec), 2)
FROM read_parquet('benchmark_telecom_cdrs.parquet');
```
* **Performance:** **14.00 ms**.
* By reading only 2 columns out of 10, DuckDB bypasses 80% of disk I/O, achieving extreme throughput.

---

### Benchmark 3: Analytical Window Functions (Time-Series Smoothing)
Computing rolling diurnal traffic smoothing across 10 regions:
```sql
SELECT 
    record_id,
    location_region,
    session_duration_sec,
    ROUND(AVG(session_duration_sec) OVER (
        PARTITION BY location_region 
        ORDER BY event_timestamp_utc 
        ROWS BETWEEN 5 PRECEDING AND 5 FOLLOWING
    ), 2) AS rolling_avg_duration
FROM read_parquet('benchmark_telecom_cdrs.parquet')
LIMIT 1000;
```
* **Performance:** **116.94 ms** across 1M records.

---

### Benchmark 4: The Out-Of-Core Stress Test (32MB RAM Cap)
Traditional tools like Pandas fail when datasets exceed available RAM. To test DuckDB's resilience, we restricted available memory to an artificial **32 MB**:
```python
con = duckdb.connect()
con.execute("SET max_memory = '32MB'")
con.execute("""
    SELECT user_agent_device, COUNT(*), ROUND(SUM(amount_tzs), 2)
    FROM read_parquet('benchmark_telecom_cdrs.parquet')
    GROUP BY user_agent_device
""").fetchall()
```
* **Result:** **PASSED (18.08 ms)**. DuckDB dynamically streams chunks through vectorized pipelines with zero out-of-memory errors.

---

### Benchmark 5: Persistent Storage & Sub-Millisecond Point Queries
Saving the 1M dataset to native DuckDB columnar format (`.duckdb`):
* **Raw CSV Size:** ~125 MB
* **Snappy Parquet Size:** 35.39 MB
* **Native DuckDB File:** **25.76 MB (4.8x compression ratio)**
* **Subsequent Point Query Speed:** **0.82 ms** (instantaneous interactive analytics).

---

## How to Run the Benchmark

```bash
python3 benchmark_duckdb_vs_pandas.py
```

Outputs:
- Generates `benchmark_telecom_cdrs.parquet` (1M rows).
- Runs 5 automated benchmarks.
- Exports structured performance metrics to `duckdb_benchmark_results.json`.
