import boto3
import botocore
import os
from ec2_resource import ec2_client
from dotenv import load_dotenv

load_dotenv()

ec2 = ec2_client()
SECURITY_GROUP_NAME = os.getenv('SECURITY_GROUP_NAME')
VPC_NAME = os.getenv('VPC_NAME')
CIDR_BLOCK = os.getenv('CIDR_BLOCK')

def create_vpc():
    print("! Creating VPC ")
    vpc_response = ec2.create_vpc(
    CidrBlock = CIDR_BLOCK,
    InstanceTenancy = 'dedicated',
    TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ],
    )
    vpc = vpc_response["Vpc"]["VpcId"]
    print("+ Created VPC id=",vpc)
    return vpc

def create_security_group():
    try:
        print("! Crearing security group")
        response_security_group = ec2.create_security_group(
                Description = 'boto3 ssh vpc',
                GroupName = SECURITY_GROUP_NAME,
                VpcId = create_vpc(),
                TagSpecifications=[
                    {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'boto3-ec2',
                            'Value': 'foo-bar'
                        },
                    ]
                    },
                ],
            )
        print("+ Created security group id=",response_security_group["GroupId"])

    except botocore.exceptions.ClientError as e:
        print(":: Error :",e)


if __name__ == "__main__":
    create_security_group()