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
        return False

def check_security_group_existence(vpc_id: str):
    print(f"! Checking if {SECURITY_GROUP_NAME} already exists")
    response = ec2.describe_security_groups(
    Filters=[
        {"Name": "vpc-id", "Values": [vpc_id]},
        {"Name": "group-name", "Values":[SECURITY_GROUP_NAME]}
    ])
    sg_list = response["SecurityGroups"]
    if(sg_list):
        sg_id = response["SecurityGroups"][0]["GroupId"]    
        print(f"! Security Group {SECURITY_GROUP_NAME} exists")
        return True
    else:
        print(f"! Security Group {SECURITY_GROUP_NAME} doesn't exist, Creating one.")
        return False

def check_igw_existence(vpc_id: str):
    print(f"! checking if internet-gateway exists for {VPC_NAME} ")
    response = ec2.describe_internet_gateways(
        Filters = [
            {"Name": "attachment.vpc-id", "Values": [vpc_id]}
        ]
    )
    igw_id = response['InternetGateways'][0]['InternetGatewayId']
    if(igw_id):
        return igw_id
    else:
        return False

def create_vpc():
    vpc_id = check_vpc_existence()
    if(vpc_id):
        return vpc_id
    else:
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
    security_group_existence = check_security_group_existence(vpc_id)
    if(security_group_existence):
        return True
    
    else:
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
            return True


        except botocore.exceptions.ClientError as e:
            print(":: Error :",e)


def create_internet_gateway(vpc_id: str):
    igw_existence = check_igw_existence(vpc_id)
    if(igw_existence):
        print(f"! Internet-gateway id={igw_existence} exists for vpc {VPC_NAME}")
        return igw_existence
    else:
        print(f"! Creating internet-gateway for {VPC_NAME}")
        response = ec2.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'boto3-ec2',
                            'Value': 'foo-bar'
                        },
                    ]
                }
            ]
        )
        igw_id = response['InternetGateway']['InternetGatewayId']
        print(f"+ Created internet-gateway id={igw_id} for {VPC_NAME}")
        return igw_id
    

if __name__ == "__main__":
    os.system('clear')
    vpc_id = create_vpc()
    sg_id = create_security_group(vpc_id)
    igw_id = create_internet_gateway(vpc_id)
