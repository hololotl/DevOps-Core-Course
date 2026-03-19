# Lab 6: Advanced Ansible & CI/CD - Submission

**Name:** Niyaz  
**Date:** 2026-03-05  
**Lab Points:** 10/10 (core tasks)

---

## 1) Overview
Implemented advanced Ansible automation with:
- blocks/rescue/always
- tags for selective execution
- Docker Compose deployment (Jinja2 template)
- safe wipe logic (variable + tag)
- GitHub Actions CI/CD (lint + deploy + verify)

---

## 2) Blocks & Tags
Updated roles:
- `common`: package/user blocks, rescue + always, tags `packages`, `users`, role tag `common`
- `docker`: install/config blocks, retry logic, always ensure Docker service, tags `docker_install`, `docker_config`, role tag `docker`

Execution examples tested:
- `--tags docker`
- `--skip-tags common`
- `--tags docker_install`
- `--list-tags`

---

## 3) Docker Compose Migration
- Renamed role `app_deploy` → `web_app`
- Added Compose template with dynamic variables
- Added role dependency: `web_app` depends on `docker`
- Deployment moved from `docker run` style to `community.docker.docker_compose_v2`
- Health check included in role

Result: app runs via Compose and is reachable on host port `8000`.

---

## 4) Wipe Logic
Implemented safe wipe in `roles/web_app/tasks/wipe.yml`.
- Control variable: `web_app_wipe: false` (default)
- Wipe tag: `web_app_wipe`
- Include order: wipe first, then deploy

Scenarios tested:
1. Normal deploy (wipe skipped)
2. Wipe only (tag + variable)
3. Clean reinstall (wipe → deploy)
4. Safety check (tag only + variable false)

---

## 5) CI/CD Integration
Created workflow: `.github/workflows/ansible-deploy.yml`
- Trigger on Ansible path changes
- Lint job: `ansible-lint`
- Deploy job: `ansible-playbook`
- Verify job: app health endpoint check

Added Actions badge in Ansible README.

---

## 6) Testing Results
- Selective tag execution: passed
- Rescue/always behavior: passed
- Compose deployment: passed
- Wipe logic scenarios: passed
- CI/CD workflow after fixes: passed
- App accessibility:
  - `curl http://localhost:8000`
  - `curl http://<vm_ip>:8000`

---

## 7) Challenges & Fixes
- Docker image tag mismatch (`latest` vs `1.0.0`) → fixed variable
- Container name conflict from old deployment → migration cleanup logic
- CI verify step instability → aligned port/check logic
- ansible-lint issues (FQCN, truthy, key-order, ignore-errors) → fixed

---

## 8) Research Answers
1. **SSH keys in GitHub Secrets risks:** secret leakage via logs/misconfig; reduce risk with least privilege, key rotation, masked outputs.
2. **Staging → Production pipeline:** separate environments, deploy to staging first, run tests, manual approval gate before production.
3. **Rollback strategy:** keep versioned image tags, store previous release, add rollback job to redeploy previous known-good tag.
4. **Self-hosted vs GitHub-hosted security:** self-hosted gives network/control isolation and tighter access policies, but requires hardening and maintenance.

---

## Summary
Lab 6 core requirements were completed: advanced role structure, Compose deployment, safe wipe mechanism, and CI/CD automation with verification.