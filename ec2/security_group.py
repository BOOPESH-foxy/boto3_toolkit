import boto3
import botocore
import os
from ec2_resource import ec2_client
from dotenv import load_dotenv

load_dotenv()

ec2 = ec2_client()
SECURITY_GROUP_NAME = os.getenv('SECURITY_GROUP_NAME')
VPC_NAME = os.getenv('VPC_NAME')

def create_vpc():
    

def create_security_group():
    try:
        response_security_group = ec2.create_security_group(
                Description = 'boto3 ssh vpc',
                GroupName = SECURITY_GROUP_NAME,
                VpcId = '',
                TagSpecifications=[
                    {
                    'ResourceType': 'security_group',
                    'Tags': [
                        {
                            'Key': 'boto3-ec2',
                            'Value': 'foo-bar'
                        },
                    ]
                    },
                ],
            )
        print(response_security_group)

    except botocore.exceptions.ClientError as e:
        print(":: Error :",e)


if __name__ == "__main__":
    create_vpc()