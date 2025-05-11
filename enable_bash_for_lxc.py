import os
import paramiko

load_dotenv()

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD")

LOCAL_SCRIPT_PATH = "enable_bash_for_lxc.sh"
REMOTE_SCRIPT_PATH = "/tmp/enable_bash_for_lxc.sh"


def main() -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PROXMOX_HOST, username=PROXMOX_USER, password=PROXMOX_PASSWORD)

    sftp = ssh.open_sftp()
    sftp.put(LOCAL_SCRIPT_PATH, REMOTE_SCRIPT_PATH)
    sftp.close()

    ssh.exec_command(f"chmod +x {REMOTE_SCRIPT_PATH}")
    ssh.exec_command(f"{REMOTE_SCRIPT_PATH}")

    ssh.close()


if __name__ == "__main__":
    main()
