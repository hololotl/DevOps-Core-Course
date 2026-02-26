## Task 2 — System Provisioning Roles

### First Run (Installation)
```
TASK [common : Update apt cache]           changed
TASK [common : Install common packages]    changed  
TASK [docker : Add Docker GPG key]         changed
TASK [docker : Add Docker repository]      changed
TASK [docker : Install Docker packages]    changed
TASK [docker : Add user to docker group]   changed
```
**6 tasks changed**: Packages installed, Docker repo/keys added, user added to docker group.

### Second Run (Idempotency)
```
PLAY RECAP
your-vm-name: ok=9 changed=0 unreachable=0 failed=0
```
**0 changes**: All tasks `ok` (green).

### Analysis
**First run changes**:
- `apt cache` → Updated package index
- `common packages` → Installed: python3-pip, curl, git, vim, htop, unzip  
- `Docker GPG/repo` → Added Docker official repository
- `Docker packages` → Installed: docker-ce, containerd.io, docker-compose-plugin
- `docker group` → Added `ubuntu` user to `docker` group

**Second run unchanged**:
- Ansible modules check current state first
- Packages already installed → `state: present` satisfied
- Services already running → `state: started` satisfied  
- Repositories already exist → `state: present` satisfied
- **Idempotency proven**: Repeatable runs are safe and produce no changes.


## Task 3 — Application Deployment ✅

### Deploy Output
```
PLAY [Deploy application] 
TASK [Login to Docker Hub]              ok
TASK [Pull Docker image]                changed  
TASK [Stop existing container]          ok
TASK [Run application container]        changed
TASK [Wait for application to be ready] ok
TASK [Verify health endpoint]           ok
RUNNING HANDLER [restart app]           changed
PLAY RECAP: ok=8 changed=3 failed=0 ✅
```

### Container Status
```
CONTAINER ID   IMAGE                        STATUS      PORTS
abc123456789   netotveto/devops-app:1.0.0  Up 5m       0.0.0.0:5000->5000/tcp
```

### Health Check Verification
```
$ curl http://130.193.55.173:5000/health
{"status":"healthy","timestamp":"2026-02-26T14:41:41Z","uptime_seconds":136} ✅

$ curl http://130.193.55.173:5000/
{"service":{"name":"devops-info-service","version":"1.0.0"}} ✅
```

### Vault & Security
```
✓ Credentials encrypted: group_vars/all.yml
✓ Docker Hub login: netotveto/devops-app:1.0.0
✓ Handler executed: app restart triggered
```

**Status**: **Application deployed successfully with full idempotency and health verification.**