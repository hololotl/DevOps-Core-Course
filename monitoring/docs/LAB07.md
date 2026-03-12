# LAB07 — Observability & Logging with Loki Stack

## Overview

Centralized logging stack: Loki 3.0 (storage), Promtail 3.0 (collector), Grafana 12.3 (UI), Python Flask app with JSON logging.

## Quick Start

```bash
cd monitoring
docker compose up -d
docker compose ps  # All should be healthy
```

Grafana: http://localhost:3000 (admin / grafana_admin_password)

## Setup

1. Open Grafana
2. **Connections → Data Sources → Add Loki**
3. URL: `http://loki:3100`
4. **Save & Test**
5. **Explore** → Query: `{service="app-python"}`

## Configuration

### Loki (`loki/config.yml`)

- Port 3100
- TSDB index (fast queries)
- Filesystem storage
- Retention: 7 days
- Schema v13

### Promtail (`promtail/config.yml`)

- Discovers Docker containers via socket
- Extracts labels: `container`, `stream`, `service`, `job`
- Sends to Loki on `http://loki:3100/loki/api/v1/push`
- Position tracking in `/tmp/positions.yaml`

### Docker Compose

- `loki`, `promtail`, `grafana`, `app-python` in `logging` network
- Resource limits: Loki 1GB, Grafana 1GB, Promtail 512MB, App 512MB
- Health checks on all services
- Grafana: anonymous disabled, password protected
- Volumes: `loki-data`, `grafana-data`, `promtail-positions`

## Application Logging

Python app uses `JSONFormatter` for structured logs:

```python
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': iso_timestamp,
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
        }
        for field in ('method', 'path', 'status_code', 'client_ip'):
            if hasattr(record, field):
                log_record[field] = getattr(record, field)
        return json.dumps(log_record)
```

**Logging hooks:**
- `@app.before_request` — logs method, path, client_ip
- `@app.after_request` — logs status_code
- Error handlers — log warnings/errors

**Example output:**
```json
{"timestamp": "2026-03-12T19:49:41.015046Z", "level": "INFO", "message": "Request received", "method": "GET", "path": "/health", "client_ip": "127.0.0.1"}
```

## Dashboard Panels

Query all with `{service="app-python"}`, add `| json` to parse JSON fields.

1. **Logs Table** → `{service="app-python"}`
2. **Request Rate** → `sum by (service) (rate({service="app-python"}[1m]))`
3. **Error Logs** → `{service="app-python"} | json | level="ERROR"`
4. **Log Distribution** → `sum by (level) (count_over_time({service="app-python"} | json [5m]))`

## Production Changes

- `GF_AUTH_ANONYMOUS_ENABLED: "false"` — login required
- `GF_SECURITY_ADMIN_PASSWORD` — set admin password
- `deploy.resources.limits/reservations` — CPU/memory capped
- `healthcheck:` on all services — verify readiness
- Retention 7 days — balance cost vs availability

## Testing

```bash
# Generate logs
for i in {1..20}; do curl -s http://localhost:8000/; done
for i in {1..20}; do curl -s http://localhost:8000/health; done

# Query in Grafana
{service="app-python"}
{service="app-python"} | json | level="ERROR"
{service="app-python"} | json | method="GET"
sum by (level) (count_over_time({service="app-python"} | json [5m]))
```

## Troubleshooting

```bash
# Check services
docker compose ps
docker compose logs app-python --tail=50

# Test endpoints
curl http://localhost:3100/ready
curl http://localhost:3000/api/health
curl http://localhost:8000/health

# View Promtail targets
curl http://localhost:9080/targets | grep app-python
```

## File Structure

```
monitoring/
├── docker-compose.yml
├── loki/config.yml
├── promtail/config.yml
└── docs/LAB07.md
```
