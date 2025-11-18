# 🔍 Complete Monitoring & Observability Guide

## Overview

This guide covers the complete monitoring and observability setup for 420 Python backend applications. The stack includes:

- **Prometheus** - Metrics collection and time-series database
- **Grafana** - Visualization and dashboarding
- **ELK Stack** - Elasticsearch, Logstash, Kibana for log management
- **AlertManager** - Alert routing and notification
- **Jaeger** - Distributed tracing
- **Node Exporter** - Host metrics
- **cAdvisor** - Container metrics

---

## 🏗️ Architecture

```
Applications (420 apps)
    ↓
Prometheus Scraper (Metrics)
    ↓
Prometheus TSDB
    ↓
Grafana (Visualization)
    ↓
Dashboards & Alerts

Applications (420 apps)
    ↓
Logstash (Log Processing)
    ↓
Elasticsearch (Log Storage)
    ↓
Kibana (Log Visualization)

Applications (420 apps)
    ↓
Jaeger (Trace Collection)
    ↓
Jaeger UI (Trace Visualization)
```

---

## 📋 Quick Start

### Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (optional)
- 8GB+ RAM
- 50GB+ storage

### 1. Start Monitoring Stack (Docker Compose)

```bash
# Navigate to project directory
cd /home/user/02-python-app

# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Verify services are running
docker-compose -f docker-compose.monitoring.yml ps
```

### 2. Access Services

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **AlertManager** | http://localhost:9093 | - |
| **Kibana** | http://localhost:5601 | - |
| **Jaeger** | http://localhost:16686 | - |
| **cAdvisor** | http://localhost:8080 | - |

### 3. Configure Applications

Update your `main.py` to include metrics:

```python
from fastapi import FastAPI
from app.core.metrics import setup_metrics_endpoint

app = FastAPI()

# Setup metrics collection
setup_metrics_endpoint(app, app_name="my-app", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 4. Update requirements.txt

```bash
# Add to requirements.txt
prometheus-client==0.16.0
python-json-logger==2.0.4
```

---

## 📊 Prometheus Setup

### Configuration File

**Location:** `monitoring/prometheus.yml`

### Key Metrics Collected

#### HTTP Metrics
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `http_request_size_bytes` - Request size
- `http_response_size_bytes` - Response size
- `http_errors_total` - Error count

#### Database Metrics
- `db_query_duration_seconds` - Query latency
- `db_query_errors_total` - Query errors
- `db_connections_active` - Active connections
- `db_connection_pool_size` - Pool size

#### Cache Metrics
- `cache_hits_total` - Cache hits
- `cache_misses_total` - Cache misses
- `cache_duration_seconds` - Cache operation latency

#### Application Health
- `app_version_info` - Application version
- `app_uptime_seconds` - Application uptime
- `active_users` - Active user count
- `requests_queued` - Queued requests

### Queries Examples

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_errors_total[5m])

# Request size distribution
histogram_quantile(0.50, rate(http_request_size_bytes_bucket[5m]))

# Database query latency
histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))

# Cache hit ratio
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Active database connections
db_connections_active

# Active users
active_users
```

---

## 📈 Grafana Setup

### Auto-Provisioning

Dashboards and datasources are automatically provisioned:

**Location:** `monitoring/grafana/provisioning/`

### Available Dashboards

1. **Application Overview** - Request rate, latency, errors, active users
2. **Database Performance** - Query latency, errors, connection pool
3. **Cache Performance** - Hit ratio, operation latency
4. **Infrastructure** - CPU, memory, disk, network
5. **Container Metrics** - Container resource usage
6. **Kubernetes Metrics** - K8s cluster health (if using K8s)

### Creating Custom Dashboards

1. Access Grafana: http://localhost:3000
2. Login: admin / admin123
3. Create new dashboard
4. Add panels with Prometheus queries
5. Set time range and refresh interval

### Example Dashboard Panel

**Request Rate Panel:**
```
Query: rate(http_requests_total[5m])
Legend: {{ method }} {{ endpoint }}
Format: Time series
```

**Latency Panel:**
```
Query: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
Legend: {{ method }} {{ endpoint }}
Format: Time series
```

---

## 🚨 Alert Rules

### Location

`monitoring/alert_rules.yml`

### Alert Categories

#### 🔴 Critical Alerts

- **HighErrorRate** - Error rate > 5%
- **InstanceDown** - Service unavailable
- **HighDatabaseErrorRate** - DB errors > 1%
- **DatabasePoolNearCapacity** - Connections > 80%

#### 🟠 Warning Alerts

- **HighLatency** - P95 latency > 1 second
- **HighMemoryUsage** - Memory > 85%
- **HighCPUUsage** - CPU > 80%
- **DiskUsageHigh** - Disk > 85%
- **LowCacheHitRatio** - Cache hit ratio < 50%

#### 🔵 Info Alerts

- **HighConcurrentUsers** - Users > 10,000
- **QueueBacklogGrowing** - Growing queue

### AlertManager Configuration

**Location:** `monitoring/alertmanager.yml`

**Notification Channels:**
- Slack
- PagerDuty
- Email
- Webhook

### Configure Slack Notifications

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Update `alertmanager.yml`:
   ```yaml
   global:
     slack_api_url: 'YOUR_WEBHOOK_URL'
   ```
3. Restart AlertManager:
   ```bash
   docker-compose -f docker-compose.monitoring.yml restart alertmanager
   ```

---

## 📝 ELK Stack (Logging)

### Components

- **Elasticsearch** - Log storage and indexing
- **Logstash** - Log processing and shipping
- **Kibana** - Log visualization

### Log Format

Applications should send JSON logs:

```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "logger": "application",
  "message": "Request processed",
  "request_id": "550e8400-e29b-41d4",
  "duration_ms": 145
}
```

### Sending Logs to Logstash

```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Logs will be automatically sent to Logstash
logger.info("Event occurred", extra={"user_id": 123, "action": "login"})
```

### Kibana Index Patterns

1. Access Kibana: http://localhost:5601
2. Create index pattern: `logs-*`
3. Time field: `@timestamp`
4. Create visualizations and dashboards

### Log Queries (Lucene Syntax)

```
# All errors
level:"ERROR"

# Specific application
logger:"app_name"

# High latency requests
duration_ms:>1000

# Specific endpoint
endpoint:"/api/users"

# Time range
@timestamp:[2024-01-15T10:00:00 TO 2024-01-15T11:00:00]
```

---

## 🔗 Distributed Tracing (Jaeger)

### Setup Applications

```python
from jaeger_client import Config
from opentracing.propagation import Format

def init_jaeger_tracer(service_name, validate_port=6831):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()

tracer = init_jaeger_tracer('my-app')
```

### Instrument FastAPI

```python
from fastapi import FastAPI
from jaeger_client import Config
from opentracing_instrumentation.local_span import get_active_span

app = FastAPI()

# Initialize Jaeger
tracer = init_jaeger_tracer('my-app')

# Create spans
with tracer.start_active_span('operation_name') as scope:
    span = scope.span
    span.set_tag('http.method', 'GET')
    span.set_tag('http.url', '/api/endpoint')
    # Your operation here
```

### View Traces

Access Jaeger UI: http://localhost:16686

---

## 🐳 Kubernetes Deployment

### Prerequisites

```bash
# Install Prometheus Operator (recommended)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

### Apply Manifests

```bash
# Create monitoring namespace and configure Prometheus
kubectl apply -f monitoring/kubernetes/monitoring-namespace.yaml

# Deploy Prometheus
kubectl apply -f monitoring/kubernetes/prometheus-deployment.yaml

# Deploy Grafana
kubectl apply -f monitoring/kubernetes/grafana-deployment.yaml

# Deploy AlertManager
kubectl apply -f monitoring/kubernetes/alertmanager-deployment.yaml
```

### Port Forwarding

```bash
# Prometheus
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Grafana
kubectl port-forward -n monitoring svc/grafana-service 3000:3000

# AlertManager
kubectl port-forward -n monitoring svc/alertmanager-service 9093:9093
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n monitoring

# Check services
kubectl get svc -n monitoring

# Check Prometheus targets
kubectl exec -n monitoring prometheus-0 -- curl localhost:9090/api/v1/targets
```

---

## 📊 Best Practices

### 1. Metrics

- Use meaningful metric names
- Add labels for dimensionality
- Cardinality awareness (avoid unbounded labels)
- Keep metrics focused and actionable

### 2. Alerts

- Alert on symptoms, not causes
- Set appropriate thresholds
- Route alerts to right teams
- Include runbooks in alert descriptions
- Test alert firing and notifications

### 3. Dashboards

- Keep dashboards simple and focused
- Use consistent time ranges
- Create dashboards for different audiences:
  - Executive (SLA/KPI focused)
  - Operations (System health)
  - Development (Detailed metrics)

### 4. Logging

- Use structured logging (JSON)
- Include context (request ID, user ID, etc.)
- Set appropriate log levels
- Archive old logs to S3 or similar

### 5. Retention

- Prometheus: 30 days (configurable)
- Elasticsearch: 7-30 days (configurable)
- Long-term: Archive to S3/GCS

---

## 🔧 Troubleshooting

### Prometheus Issues

```bash
# Check if Prometheus is scraping targets
curl http://localhost:9090/api/v1/targets

# Check scrape errors
curl http://localhost:9090/api/v1/targets?state=any

# Reload configuration
curl -X POST http://localhost:9090/-/reload
```

### Grafana Issues

```bash
# Check logs
docker logs grafana

# Reset admin password
docker exec grafana grafana-cli admin reset-admin-password newpassword
```

### Elasticsearch Issues

```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# Check indices
curl http://localhost:9200/_cat/indices

# Delete old indices
curl -X DELETE http://localhost:9200/logs-2024.01.01
```

### AlertManager Issues

```bash
# Check configuration
curl http://localhost:9093/api/v1/status

# Reload configuration
curl -X POST http://localhost:9093/-/reload

# Check alerts
curl http://localhost:9093/api/v1/alerts
```

---

## 📈 Scalability

### Multi-Cluster Monitoring

Use **Thanos** or **Prometheus Federation** for:
- Deduplication across clusters
- Long-term storage
- Global querying

### High-Volume Logging

Use **Loki** instead of ELK for:
- Lower resource footprint
- Better label-based indexing
- Simpler setup

### Distributed Tracing at Scale

Use **Tempo** for:
- Cost-effective trace storage
- Scalable retention
- Integration with Prometheus

---

## 📚 Resources

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [Elasticsearch Docs](https://www.elastic.co/guide/index.html)
- [Jaeger Docs](https://www.jaegertracing.io/docs/)

---

## ✅ Checklist

- [ ] Docker Compose monitoring stack running
- [ ] Prometheus scraping metrics
- [ ] Grafana dashboards created
- [ ] Alerts configured
- [ ] Slack notifications working
- [ ] Logstash processing logs
- [ ] Kibana dashboards created
- [ ] Jaeger collecting traces
- [ ] Kubernetes manifests deployed (if using K8s)
- [ ] Documentation reviewed

---

**Last Updated:** 2024-01-15
**Version:** 1.0.0
**Maintained By:** DevOps Team
