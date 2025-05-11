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

    commands = [
        f"chmod +x {REMOTE_SCRIPT_PATH}",
        f"{REMOTE_SCRIPT_PATH}",
    ]

    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(f'Command "{command}" output:')
        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh.close()


if __name__ == "__main__":
    main()
