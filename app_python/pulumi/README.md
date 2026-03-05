# Pulumi Yandex Cloud Infrastructure

Pulumi Python project recreating Task 1 Terraform infrastructure for **DevOps-Core-Course Lab 4**.

---

## 📋 Overview

**9 Resources:**
- 🌐 **VPC Network** (192.168.10.0/24)
- 🔹 **Subnet** (ru-central1-b)
- 🛡️ **Security Group** (SSH:22, HTTP:80, App:5000)
- 🖥️ **Compute Instance** (2vCPU/20%/1GB, Ubuntu)

---

## ✅ Prerequisites

| Requirement | Description |
|-------------|-------------|
| **Pulumi CLI** | `pulumi version` |
| **Yandex Cloud** | Folder: `b1g2uppn3rh1bt5kdmv8`, IAM token configured |
| **Python 3.11** | `python3.11 -m venv venv` (Python 3.12 incompatible) |
| **SSH Key** | `~/.ssh/id_ed25519.pub` |

---

## 🚀 Setup

```bash
cd pulumi
source venv/bin/activate
pip install pulumi pulumi_yandex
pulumi stack select dev
```

### Configuration

```bash
pulumi config set yandex:folder_id b1g2uppn3rh1bt5kdmv8
pulumi config set yandex:token y0_AgAAAAE... --secret
```

---

## ⚡ Quick Start

```bash
# Preview changes (9 resources ✓)
pulumi preview

# Create infrastructure
pulumi up

# Get VM public IP
pulumi stack output vm_public_ip

# Connect via SSH
ssh -i ~/.ssh/id_ed25519 ubuntu@<IP>
```

---

## 📤 Outputs

```text
vm_id: epdxxxxxx
vm_public_ip: 51.250.xxx.xxx  ← SSH HERE
vpc_id: enpxxxxxx
```

---

## 🔧 Key Fixes Applied

| Issue | Solution |
|-------|----------|
| **Python 3.12 incompatibility** | Use Python 3.11 (3.12 breaks `pkg_resources`) |
| **Security Groups** | Use `security_group_binding` (not `security_group_id`) |
| **SSH Path** | `os.path.expanduser("~/.ssh/id_ed25519.pub")` |

---

## ⚖️ Terraform vs Pulumi

| Aspect | Terraform HCL | Pulumi Python |
|--------|---------------|---------------|
| **Language** | Domain-specific | Full Python |
| **IDE Support** | Poor | Full IntelliSense |
| **Logic** | Static | Dynamic |
| **Errors** | Runtime | IDE-detected |

**Preference:** Pulumi - better dev experience despite provider quirks.

---

## 🧹 Cleanup

```bash
pulumi destroy
```

---

## 📝 Lab Report Summary

```text
- ✓ Terraform destroyed
- ✓ Pulumi: 9 resources created  
- ✓ VM: 2vCPU/1GB ru-central1-b, Public IP from pulumi up
- ✓ SSH verified: ubuntu@<IP>
- ✓ Fixed: Python 3.11 + SecurityGroupRule binding
```

---

