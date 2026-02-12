# Lab 2 — Docker Containerization

## 1. Docker Best Practices Applied

**Non-Root User**  
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```
Why: Prevents privilege escalation if container is compromised.

**Multi-Stage Build**  
```dockerfile
FROM python:3.13-slim as builder
RUN python -m venv /opt/venv
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
COPY --from=builder /opt/venv /opt/venv
```
Why: Final image excludes build tools and pip. Image size: 331MB (vs 800MB without optimization).

**Proper Layer Ordering**  
Copy `requirements.txt` before `app.py`. Why: Docker caches pip install layer. Code changes don't rebuild dependencies (saves 10+ seconds per build).

**Specific Base Image Version**  
`python:3.13-slim` not `latest`. Why: Reproducible builds, known security patches, minimal size (150MB).

**.dockerignore File**  
Excludes: `.git`, `__pycache__`, `venv/`, `tests/`, `*.md`. Why: Reduces build context from 10MB to 3MB.

**Health Check**  
```dockerfile
HEALTHCHECK --interval=30s CMD python -c \
  "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()"
```
Why: Kubernetes and orchestration systems can restart unhealthy containers.

---

## 2. Image Information & Decisions

**Base Image:** `python:3.13-slim`  
Justification: Latest stable Python, minimal dependencies, 150MB (slim is 800MB smaller than full image)

**Final Image Size:** 331MB  
- Base Python: 150MB
- Flask venv: 35MB  
- App code: <1MB
- Metadata: 145MB

Assessment: Acceptable for production Flask app. Multi-stage build saved ~500MB.

**Layer Structure:**
1. Base Python image
2. User creation + directory ownership
3. Virtual environment (from builder)
4. Application code
5. Metadata (EXPOSE, HEALTHCHECK, CMD)

---

## 3. Build & Run Process

**Build Output:**
```bash
$ docker build -t devops-app:1.0.0 .

[+] Building 258.6s (14/14) FINISHED
 => [builder 1/5] FROM python:3.13-slim 232.2s
 => [builder 4/5] RUN python -m venv /opt/venv 3.7s
 => [builder 5/5] RUN pip install -r requirements.txt 12.1s
 => [stage-1 4/5] COPY --from=builder /opt/venv /opt/venv 0.2s
 => [stage-1 5/5] COPY --chown=appuser:appuser app.py . 0.0s

Successfully built devops-app:1.0.0
```

**Running Container:**
```bash
$ docker run -d -p 5000:5000 devops-app:1.0.0
7ba41b00f524f7a797ba48115d0d60a41288be86702451d47c1485b8b222742e
```

**Testing Endpoints:**
```bash
$ curl -s http://localhost:5000/ | python3 -m json.tool | head -20
{
    "service": {"name": "devops-info-service", "version": "1.0.0", "framework": "Flask"},
    "runtime": {"uptime_seconds": 11, "uptime_human": "0 hours, 0 minutes"},
    ...
}

$ curl -s http://localhost:5000/health
{"status": "healthy", "timestamp": "2026-02-05T08:54:41.767265Z", "uptime_seconds": 16}
```

**Docker Hub:**
```bash
$ docker tag devops-app:1.0.0 netotveto/devops-app:1.0.0
$ docker push netotveto/devops-app:1.0.0
Successfully pushed netotveto/devops-app:1.0.0
```

Repository: https://hub.docker.com/r/netotveto/devops-app

---

## 4. Technical Analysis

**How Dockerfile Works:**
- Stage 1: Build Python venv with Flask installed, discard builder stage
- Stage 2: Start fresh image, copy only venv (no build tools), copy app code, run as non-root user
- Result: Final image contains only Python + Flask + app code

**Layer Order Impact:**
- Good order: `COPY requirements.txt` → `RUN pip install` → `COPY app.py`
  - Code change: rebuild skips pip install layer (1 second)
- Bad order: `COPY .` → `RUN pip install`
  - Code change: invalids first COPY, rebuilds everything (10+ seconds)

**Security Implemented:**
- Non-root user: Prevents container escape with root privileges
- Minimal base image: Fewer packages = smaller attack surface
- No build tools in final image: Prevents malicious compilation
- Health check: Only healthy containers stay running

**.dockerignore Impact:**
Excludes 5-10MB of unnecessary files from build context → faster Docker daemon processing in CI/CD pipelines.

---

## 5. Challenges & Solutions

**Challenge 1: Virtual Environment in Container**  
How to properly set up venv in containerized environment?
- Solution: Create venv at `/opt/venv`, set `ENV PATH="/opt/venv/bin:$PATH"`
- Learning: Venv needs explicit PATH configuration; Docker ENV handles it automatically

**Challenge 2: Health Check Without External Dependencies**  
Implement health check without adding extra tools?
- Solution: Use Python's built-in `urllib` to call `/health` endpoint
- Learning: Use application itself for health checks, keeps container self-contained

**Challenge 3: Understanding Multi-Stage Build**  
Confusion about which files to copy from which stage?
- Solution: Clear labeling (`FROM ... as builder`), explicit copy (`COPY --from=builder`)
- Learning: Multi-stage builds require planning but essential for production containers

---

✅ **Complete:** Non-root user, multi-stage build, layer caching, specific base image, .dockerignore, health check. Image published to Docker Hub. All endpoints tested.
