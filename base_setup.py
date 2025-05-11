import os
import paramiko
import json
import time
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD")
SSH_PUB_KEY_PATH = os.getenv("SSH_PUB_KEY_PATH")


def enable_bash_for_lxc(ssh: paramiko.SSHClient) -> None:
    with open("containers.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for name, id in data.items():
        ssh.exec_command(f"echo 'lxc.init.cmd: /bin/bash' >> /etc/pve/lxc/{id}.conf")
        ssh.exec_command(f"pct restart {id}")
        print(f"Waiting for restart of {name} ({id})")
        time.sleep(10)


def main() -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PROXMOX_HOST, username=PROXMOX_USER, password=PROXMOX_PASSWORD)

    enable_bash_for_lxc(ssh)

    ssh.close()


if __name__ == "__main__":
    main()
