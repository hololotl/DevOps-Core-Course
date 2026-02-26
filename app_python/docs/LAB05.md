# LAB05 — Ansible Fundamentals

## 1. Architecture Overview

**Ansible**: `2.16+`  
**Target VM**: Ubuntu 24.04 LTS (`compute-vm-2-2-10-ssd`)  
**Structure**:
```
ansible/
├── inventory/hosts.ini      [webservers]
├── roles/                   common, docker, app_deploy
├── playbooks/              provision.yml, deploy.yml, site.yml
├── group_vars/all.yml      (Vault encrypted)
└── ansible.cfg
```

**Why Roles?** Modular, reusable, self-contained. Easier to test, share, and maintain vs monolithic playbooks.

## 2. Roles Documentation

### **common**
**Purpose**: Install essential system packages  
**Variables**: `common_packages: [python3-pip, curl, git, vim, htop, unzip]`  
**Handlers**: None  
**Dependencies**: None

### **docker**  
**Purpose**: Install Docker CE + add user to docker group
**Variables**: `docker_user: ubuntu`  
**Handlers**: `restart docker`  
**Dependencies**: `common` (apt repositories)

### **app_deploy**
**Purpose**: Deploy `netotveto/devops-app:1.0.0` container  
**Variables**: `app_port: 5000`, `restart_policy: unless-stopped`  
**Handlers**: `restart app`  
**Dependencies**: `docker`

## 3. Idempotency Demonstration

### **First Run** (provision.yml):
```
TASK [common: Update apt]     changed ✓
TASK [common: Packages]       changed ✓  
TASK [docker: GPG key]        changed ✓
TASK [docker: Repository]     changed ✓
TASK [docker: Packages]       changed ✓
TASK [docker: User group]     changed ✓
PLAY RECAP: ok=9 changed=6
```

### **Second Run**:
```
PLAY RECAP: ok=9 changed=0 ✅
```

**Analysis**: First run installs packages/services. Second run finds everything present → no changes.

## 4. Ansible Vault Usage

**Storage**: `group_vars/all.yml` (encrypted):
```
$ ansible-vault view group_vars/all.yml
---
dockerhub_username: netotveto ✳
dockerhub_password: dckr_pat_6dRe8t ✳
```
**Password**: Managed locally, `--ask-vault-pass` for CI/CD  
**Why Vault**: Secrets never stored in plaintext, git-safe encryption.

## 5. Deployment Verification

### **deploy.yml Output**:
```
TASK [Login Docker Hub]         ok
TASK [Pull image]              changed ✓
TASK [Run container]           changed ✓  
TASK [Health check]             ok ✓
PLAY RECAP: ok=8 changed=3 ✓
```

### **Container Status**:
```
CONTAINER ID   netotveto/devops-app:1.0.0  Up 5m  0.0.0.0:5000->5000/tcp
```

### **Health Checks**:
```
$ curl http://130.193.55.173:5000/health
{"status":"healthy","uptime_seconds":153} ✓

$ curl http://130.193.55.173:5000/
{"service":{"name":"devops-info-service","version":"1.0.0"}} ✓
```

## 6. Key Decisions

**Roles vs Playbooks**: Roles = reusable modules. Playbooks = orchestration.  
**Reusability**: Roles can be shared across projects/environments.  
**Idempotency**: `state: present`, checks before changes.  
**Handlers**: Only trigger on actual changes → efficient.  
**Vault**: Secrets encrypted at rest, injected at runtime.

## 7. Challenges Solved

- **Ubuntu 24.04 pip error**: `pip` → `apt install python3-docker`  
- **Vault path issue**: `../group_vars/all.yml` relative path  
- **Docker image 404**: `latest` → `1.0.0` existing tag  
- **docker_user**: Ansible uses `ubuntu`, SSH used `niyaz` → `sudo docker ps`

***

**Status**: ✅ **Full infrastructure provisioned + app deployed with idempotency & security**