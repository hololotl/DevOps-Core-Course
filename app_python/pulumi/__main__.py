import pulumi
import pulumi_yandex as yandex

# Конфигурация
folder_id = pulumi.Config("yandex").require("folder_id")
zone = "ru-central1-b"
vm_name = "pulumi-lab-vm"

# Сеть VPC
vpc_network = yandex.VpcNetwork("lab-vpc",
    name="pulumi-lab-vpc")

# Субнет
subnet = yandex.VpcSubnet("lab-subnet",
    name="pulumi-lab-subnet",
    zone=zone,
    network_id=vpc_network.id,
    v4_cidr_blocks=["192.168.10.0/24"])

# Security Group (БЕЗ ingress/egress)
sg = yandex.VpcSecurityGroup("lab-sg",
    name="pulumi-lab-sg",
    network_id=vpc_network.id)

# Правила Security Group (с security_group_binding)
ssh_rule = yandex.VpcSecurityGroupRule("lab-sg-ssh",
    security_group_binding=sg.id,  # ← ИЗМЕНИЛИ НА ЭТО
    direction="ingress",
    description="SSH",
    v4_cidr_blocks=["0.0.0.0/0"],
    protocol="TCP",
    from_port=22,
    to_port=22)

http_rule = yandex.VpcSecurityGroupRule("lab-sg-http",
    security_group_binding=sg.id,  # ← ИЗМЕНИЛИ НА ЭТО
    direction="ingress",
    description="HTTP",
    v4_cidr_blocks=["0.0.0.0/0"],
    protocol="TCP",
    from_port=80,
    to_port=80)

app_rule = yandex.VpcSecurityGroupRule("lab-sg-app",
    security_group_binding=sg.id,  # ← ИЗМЕНИЛИ НА ЭТО
    direction="ingress",
    description="App port 5000",
    v4_cidr_blocks=["0.0.0.0/0"],
    protocol="TCP",
    from_port=5000,
    to_port=5000)

egress_rule = yandex.VpcSecurityGroupRule("lab-sg-egress",
    security_group_binding=sg.id,  # ← ИЗМЕНИЛИ НА ЭТО
    direction="egress",
    description="All egress",
    v4_cidr_blocks=["0.0.0.0/0"],
    protocol="ANY")

vm = yandex.ComputeInstance("lab-vm",
    name=vm_name,
    folder_id=folder_id,
    zone=zone,
    platform_id="standard-v2",
    resources=yandex.ComputeInstanceResourcesArgs(
        cores=2,
        core_fraction=20,
        memory=1
    ),
    boot_disk=yandex.ComputeInstanceBootDiskArgs(
        initialize_params=yandex.ComputeInstanceBootDiskInitializeParamsArgs(
            image_id="fd80mrhj8fl2oe87o4e1"
        )
    ),
    network_interfaces=[yandex.ComputeInstanceNetworkInterfaceArgs(
        subnet_id=subnet.id,
        security_group_ids=[sg.id],
        nat=True
    )],
    metadata={
        "ssh-keys": open("/home/niyaz/.ssh/id_ed25519.pub").read()
    },
    labels={
        "lab": "devops-core",
        "tool": "pulumi"
    })
# Outputs
pulumi.export("vm_id", vm.id)
pulumi.export("vm_public_ip", vm.network_interfaces[0].nat_ip_address)
pulumi.export("vpc_id", vpc_network.id)
