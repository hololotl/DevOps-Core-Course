Cloud Provider

Yandex Cloud - selected for Russia accessibility and free tier availability.
Terraform Version


Terraform v1.9.5
+ provider registry.terraform.io/yandex-cloud/yandex v0.189.0

VM Configuration

    Name: compute-vm-2-2-10-ssd-1772041765753

    Zone: ru-central1-b

    Platform: Intel Ice Lake

    Resources: 2 vCPU (100%), 2 GB RAM, 10 GB SSD

    OS: Ubuntu 24.04 LTS

    External IP: 130.193.55.173

SSH Access

bash
ssh niyaz@130.193.55.173

Terraform Output


$ terraform output
vm_id = "epd8vgorh3gnhnvpqior"
vm_public_ip = "130.193.55.173"

Terraform Plan


data.yandex_compute_instance.existing_vm: Read complete [id=epd8vgorh3gnhnvpqior]

Changes to Outputs:
  + vm_id        = "epd8vgorh3gnhnvpqior"
  + vm_public_ip = "130.193.55.173"

Plan: 0 to add, 0 to change, 0 to destroy.

File Structure


terraform/
├── main.tf
├── terraform.tfvars
├── .gitignore
└── README.md

Best Practices Applied

    Variables: folder_id, yandex_token, vm_name

    Outputs: vm_public_ip, vm_id

    Sensitive data protection via .gitignore

    Local state management

Cost Management

Free tier instance (0₽/month). VM preserved for Lab 5 (Ansible).