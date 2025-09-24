import os
import paramiko
from dotenv import load_dotenv
from ec2_instance import get_public_ip
load_dotenv()

KEY_FILE = os.getenv('KEY_FILE')
KEY_NAME = os.getenv('KEY_NAME')
USER_NAME = os.getenv('USER_NAME')

def ssh_ec2_instance():
    public_ip = get_public_ip()
    if(public_ip):
        key = paramiko.RSAKey.from_private_key_file(KEY_FILE,password=None)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        try:
            print(f"Connecting to {public_ip} ...")
            ssh_client.connect(hostname=public_ip, username=USER_NAME, pkey=key)
            print("Connected! Type commands (exit to quit).")

            while True:
                cmd = input(f"{USER_NAME}@{public_ip}:~$ ")
                if cmd.lower() in ["exit"]:
                    break
                if not cmd.strip():
                    continue
                stdin, stdout, stderr = ssh_client.exec_command(cmd)
                output = stdout.read().decode()
                errors = stderr.read().decode()
                if output:
                    print(output, end="")
                if errors:
                    print(errors, end="")
            ssh_client.close()
            print("::: SSH session closed :::")

        except Exception as e:
            print("SSH connection failed:", e)
