import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD")
PROXMOX_NODE = os.getenv("PROXMOX_NODE")

list_of_container_settings = [
    {
        "name": "lxc-proxy",
        "memory": 512,
        "cores": 1,
        "rootfs": "local-lvm:4",
    },
    {
        "name": "lxc-app",
        "memory": 2048,
        "cores": 2,
        "rootfs": "local-lvm:16",
    },
    {
        "name": "lxc-db",
        "memory": 4096,
        "cores": 2,
        "rootfs": "local-lvm:32",
    },
    {
        "name": "lxc-monitoring",
        "memory": 2048,
        "cores": 2,
        "rootfs": "local-lvm:16",
    },
    {
        "name": "lxc-forgejo",
        "memory": 2048,
        "cores": 2,
        "rootfs": "local-lvm:16",
    },
    {
        "name": "lxc-drone-server",
        "memory": 1024,
        "cores": 1,
        "rootfs": "local-lvm:8",
    },
    {
        "name": "lxc-drone-runner",
        "memory": 4096,
        "cores": 2,
        "rootfs": "local-lvm:16",
    },
    {
        "name": "lxc-backup",
        "memory": 2048,
        "cores": 2,
        "rootfs": "local-lvm:50",
    },
]


def init_proxmox():
    proxmox = ProxmoxAPI(
        host=PROXMOX_HOST,
        user=PROXMOX_USER,
        password=PROXMOX_PASSWORD,
        verify_ssl=False,
    )
    return proxmox


def get_next_vm_id(proxmox):
    qemu_vms = proxmox.nodes(PROXMOX_NODE).qemu.get()
    lxc_cts = proxmox.nodes(PROXMOX_NODE).lxc.get()
    qemu_ids = [vm["vmid"] for vm in qemu_vms]
    lxc_ids = [ct["vmid"] for ct in lxc_cts]
    all_ids = [int(id) for id in [*qemu_ids, *lxc_ids]]
    return max(all_ids) + 1 if all_ids else 100


def create_container(proxmox, container_settings):
    vmid = get_next_vm_id(proxmox)
    proxmox.nodes(PROXMOX_NODE).lxc.post(
        vmid=vmid,
        hostname=container_settings["name"],
        ostemplate="local:vztmpl/centos-9-stream-default_20240828_amd64.tar.xz",
        storage="local-lvm",
        memory=container_settings["memory"],
        cores=container_settings["cores"],
        net0="name=eth0,bridge=vmbr0,ip=dhcp",
        rootfs=container_settings["rootfs"],
    )


def main():
    proxmox = init_proxmox()
    for container_settings in list_of_container_settings:
        create_container(proxmox, container_settings)


if __name__ == "__main__":
    main()
