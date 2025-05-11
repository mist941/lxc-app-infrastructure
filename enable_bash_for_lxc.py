import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD")

LOCAL_SCRIPT_PATH = "enable_bash_for_lxc.sh"
LOCAL_CONTAINERS_PATH = "containers.json"
REMOTE_SCRIPT_PATH = "/tmp/enable_bash_for_lxc.sh"
REMOTE_CONTAINERS_PATH = "/tmp/containers.json"


def main() -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PROXMOX_HOST, username=PROXMOX_USER, password=PROXMOX_PASSWORD)

    sftp = ssh.open_sftp()
    sftp.put(LOCAL_SCRIPT_PATH, REMOTE_SCRIPT_PATH)
    sftp.put(LOCAL_CONTAINERS_PATH, REMOTE_CONTAINERS_PATH)
    sftp.close()

    commands = [
        f"chmod +x {REMOTE_SCRIPT_PATH}",
        f"{REMOTE_SCRIPT_PATH}",
        f"rm {REMOTE_SCRIPT_PATH}",
        f"rm {REMOTE_CONTAINERS_PATH}",
    ]

    for command in commands:
        _, stdout, stderr = ssh.exec_command(command)
        print(f'Command "{command}" output:')
        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh.close()


if __name__ == "__main__":
    main()
