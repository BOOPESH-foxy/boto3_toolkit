import botocore
import os
from ec2_resource import ec2_client
from dotenv import load_dotenv

load_dotenv()

ec2 = ec2_client()
SECURITY_GROUP_NAME = os.getenv('SECURITY_GROUP_NAME')
VPC_NAME = os.getenv('VPC_NAME')
CIDR_BLOCK = os.getenv('CIDR_BLOCK')
SSH_CIDR = os.getenv('SSH_CIDR')
REGION = os.getenv('REGION')
SUBNET_CIDR_BLOCK = os.getenv('SUBNET_CIDR_BLOCK')


def check_ec2_instance_existence():
    response_instances = ec2.describe_instances()
    print(response_instances)


def create_ec2_instaces():
    response_ec2_instance_creation = ec2.create_instance

check_ec2_instance_existence()