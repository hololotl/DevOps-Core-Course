# LAB01 — DevOps Info Service Implementation

## Framework Selection

**Chosen: Flask 3.1.0**

### Justification
Flask is lightweight and perfect for a simple info service. Fast to implement, minimal boilerplate, and sufficient for lab requirements.

### Framework Comparison

| Aspect | Flask | FastAPI | Django |
|--------|-------|---------|--------|
| Learning curve | Easy | Moderate | Steep |
| Boilerplate | Minimal | Low | High |
| Setup time | <5 min | <5 min | 10+ min |
| Good for simple apps | ✓ | ✓ | ✗ |
| Auto-docs | ✗ | ✓ | ~ |
| Production ready | ✓ | ✓ | ✓ |

---

## Best Practices Applied

### 1. Clean Code Organization
- Clear function names (`get_uptime()`, `get_system_info()`)
- Proper import grouping (stdlib → 3rd party)
- Comments only where needed

### 2. Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'Endpoint does not exist'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500
```
Returns structured JSON errors instead of HTML.

### 3. Logging
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger.info('Application starting')
logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
```
Tracks app lifecycle and request metadata.

### 4. Configuration via Environment Variables
```python
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```
Makes app configurable without code changes.

### 5. Dependencies Management
- `requirements.txt` with pinned versions for reproducibility
- `.gitignore` excludes venv, __pycache__, IDE folders, OS files

---

## API Documentation

### GET /
Returns comprehensive service and system information.

**Example Request:**
```bash
curl http://localhost:5000/ | jq
```

**Example Response:**
```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "Flask"
  },
  "system": {
    "hostname": "my-machine",
    "platform": "Linux",
    "platform_version": "...",
    "architecture": "x86_64",
    "cpu_count": 8,
    "python_version": "3.11.0"
  },
  "runtime": {
    "uptime_seconds": 300,
    "uptime_human": "0 hours, 5 minutes",
    "current_time": "2026-01-28T15:30:00Z",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "curl/7.81.0",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    {"path": "/", "method": "GET", "description": "Service information"},
    {"path": "/health", "method": "GET", "description": "Health check"}
  ]
}
```

### GET /health
Simple health check for monitoring/Kubernetes probes.

**Example Request:**
```bash
curl http://localhost:5000/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T15:30:00Z",
  "uptime_seconds": 300
}
```
Returns HTTP 200 if healthy.

---

## Testing Evidence

*(Screenshots would go here: main endpoint, health check, pretty-printed JSON)*

Testing commands:
```bash
# Main endpoint
curl -s http://localhost:5000/ | jq

# Health check
curl -s http://localhost:5000/health | jq

# Test with custom port
PORT=8080 python app.py &
curl -s http://localhost:8080/health
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| UTC timestamp formatting | Used `.isoformat().replace('+00:00', 'Z')` for ISO 8601 compliance |
| Clean JSON error responses | Implemented custom Flask error handlers returning JSON |
| Uptime calculation accuracy | Stored `START_TIME` at module load, compute delta on each request |

---
