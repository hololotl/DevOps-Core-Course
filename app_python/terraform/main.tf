terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}


provider "yandex" {
  token   = var.yandex_token
  zone = "ru-central1-b"
  folder_id = var.folder_id
}

variable "folder_id" {
  type        = string
  description = "Yandex Cloud Folder ID"
}

variable "yandex_token" {
  type        = string
  description = "Yandex Cloud OAuth token"
  sensitive   = true
}

variable "vm_name" {
  type    = string
  default = "compute-vm-2-2-10-ssd-1772041765753"
}

# Читаем существующую VM
data "yandex_compute_instance" "existing_vm" {
  folder_id = var.folder_id
  name      = var.vm_name
}

output "vm_public_ip" {
  value = data.yandex_compute_instance.existing_vm.network_interface[0].nat_ip_address
}

output "vm_id" {
  value = data.yandex_compute_instance.existing_vm.id
}
