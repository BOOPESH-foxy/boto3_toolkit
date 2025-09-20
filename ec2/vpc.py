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
SSH_CIDR = os.getenv('SSH_CIDR')


def check_vpc_existence():
    print(f"! Checking if {VPC_NAME} already exists")
    result_Vpc_exists = ec2.describe_vpcs(Filters=[{"Name":"tag:Name","Values":[VPC_NAME]}])
    vpc_list = result_Vpc_exists["Vpcs"]
    if(vpc_list):
        vpc_id = result_Vpc_exists["Vpcs"][0]["VpcId"]
        print(f"! VPC {VPC_NAME} exists")
        return vpc_id
    else:
        print(f"! Vpc {VPC_NAME} doesn't exist,Creating one.")
        vpc_id = create_vpc()
        return vpc_id



def check_security_group_existence(vpc_id: str):
    print(f"! Checking if {SECURITY_GROUP_NAME} already exists")
    print(vpc_id)
    response = ec2.describe_security_groups(
    Filters=[
        {"Name": "vpc-id", "Values": [vpc_id]},
        {"Name": "group-name", "Values":[SECURITY_GROUP_NAME]}
    ])
    sg_list = response["SecurityGroups"]
    if(sg_list):
        sg_id = response["SecurityGroups"][0]["GroupId"]    
        print(f"! Security Group {SECURITY_GROUP_NAME} exists")
        return sg_id
    else:
        print(f"! Security Group {SECURITY_GROUP_NAME} doesn't exist, Creating one.")
        create_security_group(vpc_id)


def create_vpc():
    print("! Creating VPC ")
    vpc_response = ec2.create_vpc(
    CidrBlock = CIDR_BLOCK,
    TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': VPC_NAME
                },
            ],
        },
    ],
    )
    vpc_id = vpc_response["Vpc"]["VpcId"]
    print(f"+ Created VPC id={vpc_id}")
    return vpc_id

def create_security_group(vpc_id: str):
    try:
        print("! Crearing security group")
        response_security_group = ec2.create_security_group(
                Description = 'boto3 ssh vpc',
                GroupName = SECURITY_GROUP_NAME,
                VpcId = vpc_id,
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
        sg_id = response_security_group["GroupId"]

        ec2.authorize_security_group_ingress(
            GroupId = sg_id,
            IpPermissions=[{
                "IpProtocol":"tcp",
                "FromPort":22,
                "ToPort":22,
                'IpRanges':[{'CidrIp':CIDR_BLOCK}]
            }]
        )
        print("+ Created security group id=",sg_id,f"opening 22 from {CIDR_BLOCK}")


    except botocore.exceptions.ClientError as e:
        print(":: Error :",e)


if __name__ == "__main__":
    os.system('clear')
    vpc_id = check_vpc_existence()
    sg_id = check_security_group_existence(vpc_id)