from ec2_resource import ec2_client
import os
from dotenv import load_dotenv
import stat
import botocore

load_dotenv()
ec2 = ec2_client()


KEY_FILE = os.getenv('KEY_FILE')
KEY_NAME = os.getenv('KEY_NAME')

def key_pair_generation():
    try:
        key_pair = ec2.create_key_pair(KeyName=KEY_NAME)
        print("key_pair::",key_pair)
        private_key = key_pair["KeyMaterial"]

        with open(KEY_FILE,"w") as write_file:
            write_file.write(private_key)

        os.chmod(KEY_FILE,stat.S_IRUSR | stat.S_IRUSR)
        print(f" + Saved private key to file {KEY_FILE} with (chmod 600)")
        return KEY_NAME

    except botocore.exceptions.ClientError as e:
        print(" :: Error::",e)

def check_key_pair():
    if(os.path.exists(KEY_FILE)):
        print(" :: Key-pair exists")
    else:
        print("+ Creating Key-pair")
        key_pair_generation()
