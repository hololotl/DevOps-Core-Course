# Lab 4 - Infrastructure as Code (Terraform & Pulumi) ✅

## 1. Cloud Provider & Infrastructure

**Provider**: Yandex Cloud  
**Zone**: `ru-central1-b`  
**Instance**: 2 vCPU (20% guaranteed), 1 GB RAM, Ubuntu  
**Cost**: Free tier ($0)  

**Resources created**:
- VPC Network (`192.168.10.0/24`)
- Subnet (`ru-central1-b`)
- Security Group (SSH:22, HTTP:80, App:5000)
- Compute Instance (Free tier eligible)

## 2. Terraform Implementation

**Location**: `terraform/yandex/`  
**Version**: `v1.14.3`

**Key outputs**:
```
external_ip = "130.193.55.173"
vm_id = "fhm3hpru7qnes65fso7v"
network_id = "enp91ple956fcrfvjp1r"
security_group_id = "enp39efd0jcf2lok3d48"
```

**SSH verified**: `ssh niyaz@130.193.55.173`

## 3. Pulumi Implementation ✅

**Location**: `pulumi/`  
**Version**: `v3.221.0`  
**Language**: Python 3.11 (Python 3.12 incompatible)  
**Folder ID**: `b1g2uppn3rh1bt5kdmv8`

**Pulumi preview** (9 resources):
```
+ yandex:VpcNetwork           lab-vpc
+ yandex:VpcSubnet            lab-subnet
+ yandex:VpcSecurityGroup     lab-sg
+ 4x yandex:VpcSecurityGroupRule
+ yandex:ComputeInstance      lab-vm (2vCPU/1GB)
```

**Pulumi up results** (9/9 created):
```
Resources: + 9 created

Outputs:
    vm_id: "epdrvbpugo04mb9vnqfh"
    vm_public_ip: "89.169.183.24"
    vpc_id: "enpiiukc54smb3kesoue"
```

**SSH access**:
```bash
ssh -i ~/.ssh/id_ed25519 ubuntu@89.169.183.24
```

## Key Technical Fixes Applied

1. **Python compatibility**: `setuptools==64.0.3` (pkg_resources for Python 3.12)
2. **Security Groups**: `security_group_binding` instead of `security_group_id`
3. **SSH keys**: `os.path.expanduser("~/.ssh/id_ed25519.pub")`
4. **IAM token**: Refreshed during long-running deployment (12hr limit)

## Terraform vs Pulumi Comparison

| Aspect | Terraform (HCL) | Pulumi (Python) |
|--------|-----------------|-----------------|
| **Setup time** | ✅ 2 minutes | ❌ 25 minutes |
| **Language** | Simple DSL | Full Python |
| **IDE support** | Poor | ✅ Full IntelliSense |
| **Error messages** | ✅ Clear | ❌ Cryptic |
| **Learning curve** | Easier start | Better long-term |
| **Production** | ✅ Stable | Flexible logic |

**Recommendation**: Terraform for learning IaC, Pulumi for complex automation.

## Project Structure

```
app_python/
├── terraform/yandex/     
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── pulumi/              
│   ├── __main__.py
│   ├── requirements.txt
│   └── Pulumi.yaml
└── README.md          
```

## Cleanup Commands

```bash
# Remove Pulumi infrastructure (9 resources)
cd pulumi && pulumi destroy

# Remove Terraform infrastructure  
cd ../terraform/yandex && terraform destroy
```


## 4. Terraform vs Pulumi Comparison

### Ease of Learning
**Terraform** was much easier to learn. HCL syntax is simple and declarative - you just describe what you want. Pulumi required Python 3.11 setup, package compatibility fixes, and understanding Pulumi-specific patterns.

### Code Readability  
**Terraform** wins for simple infrastructure. HCL is concise and purpose-built for IaC. **Pulumi** is more readable for complex logic (if/else, loops) but overkill for basic VM+network setup.

### Debugging  
**Terraform** debugging was straightforward - clear error messages and `terraform plan` shows exactly what changes. **Pulumi** errors were cryptic (`pkg_resources`, `ImpImporter`, `security_group_binding`) requiring extensive troubleshooting.

### Documentation  
**Terraform** has better Yandex Cloud examples and stable provider. **Pulumi** documentation is sparse, `pulumi_yandex` is outdated (2022), lacks Python 3.12 support and modern examples.

### Use Case  
**Terraform**: Simple infrastructure, learning IaC, production stability, team collaboration.  
**Pulumi**: Complex automation, multi-cloud, existing Python teams, dynamic infrastructure (if/else logic needed).



## 5  Lab 5 Preparation & Cleanup
- I will keep vm for lab 5