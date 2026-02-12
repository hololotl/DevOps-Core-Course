# LAB03 — Unit Tests (Task 1)

## Link to Ci

https://github.com/hololotl/DevOps-Core-Course/actions/runs/21955176111

## Versioning Strategy

We use Calendar Versioning (CalVer).

Format: YYYY.MM.DD (UTC build date)

Each image is tagged with:
- YYYY.MM.DD
- latest
- short commit SHA

This ensures traceability and reproducibility.

## Testing Framework
**pytest** — simple syntax, strong assertions, automatic discovery, widely used.

## Test Structure
Tests located in `app_python/tests/`.

Covered:
- `GET /` — status 200, JSON structure, required fields
- `GET /health` — status 200, health response
- `404` — proper error JSON structure

## Run Locally
```bash
cd app_python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q


## CI Best Practices applied
- **Dependency caching:** `actions/cache` used for pip cache to speed installs.
- **Fail-fast / job dependencies:** Docker publish depends on lint-and-test (`needs:`) so build only runs on success.
- **Concurrency:** Cancel outdated workflow runs (`concurrency` configured).
- **Conditional push:** Docker push runs only on `main`/`master` or on tags.
- **Security scanning:** Snyk integrated (requires `SNYK_TOKEN` secret). Snyk run is non-failing by default; set policy to fail if desired.

**Notes on measuring cache improvement:** Compare job timings in Actions tab between runs with cache miss vs cache hit (install step duration).

Required secrets:
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` — for Docker push
- `SNYK_TOKEN` — for Snyk scanning (optional)

