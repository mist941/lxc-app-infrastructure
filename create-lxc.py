import os
import json
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER") + "@pam"
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD")
PROXMOX_NODE = os.getenv("PROXMOX_NODE")
SSH_PUB_KEY_PATH = os.getenv("SSH_PUB_KEY_PATH")

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


def init_proxmox() -> ProxmoxAPI:
    proxmox = ProxmoxAPI(
        host=PROXMOX_HOST,
        user=PROXMOX_USER,
        password=PROXMOX_PASSWORD,
        verify_ssl=False,
    )
    return proxmox


def put_container_settings_in_file(name: str, id: int) -> None:
    with open("containers.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    data[name] = id

    with open("containers.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_ssh_pub_key(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def get_next_vm_id(proxmox: ProxmoxAPI) -> int:
    qemu_vms = proxmox.nodes(PROXMOX_NODE).qemu.get()
    lxc_cts = proxmox.nodes(PROXMOX_NODE).lxc.get()
    qemu_ids = [vm["vmid"] for vm in qemu_vms]
    lxc_ids = [ct["vmid"] for ct in lxc_cts]
    all_ids = [int(id) for id in [*qemu_ids, *lxc_ids]]
    return max(all_ids) + 1 if all_ids else 100


def create_container(
    proxmox: ProxmoxAPI, container_settings: dict, ssh_pub_key: str
) -> None:
    vmid = get_next_vm_id(proxmox)

    proxmox.nodes(PROXMOX_NODE).lxc.post(
        vmid=vmid,
        hostname=container_settings["name"],
        ostemplate="local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst",
        storage="local-lvm",
        memory=container_settings["memory"],
        cores=container_settings["cores"],
        net0="name=eth0,bridge=vmbr0,firewall=1,ip6=dhcp,ip=dhcp",
        rootfs=container_settings["rootfs"],
        start=1,
        features="nesting=1",
        unprivileged=1,
        **{"ssh-public-keys": ssh_pub_key},
    )

    put_container_settings_in_file(container_settings["name"], vmid)


def main() -> None:
    proxmox = init_proxmox()
    ssh_pub_key = get_ssh_pub_key(SSH_PUB_KEY_PATH)
    for container_settings in list_of_container_settings:
        create_container(proxmox, container_settings, ssh_pub_key)


if __name__ == "__main__":
    main()
