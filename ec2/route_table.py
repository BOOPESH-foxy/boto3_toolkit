import os
from ec2_resource import ec2_client
from dotenv import load_dotenv

load_dotenv()

ec2 = ec2_client()
VPC_NAME = os.getenv('VPC_NAME')

def check_route_table_existence(vpc_id: str):
    rt_response = ec2.describe_route_tables(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]}
        ]
    )
    available_route_tables = rt_response['RouteTables']
    if(available_route_tables):
        route_table_id = available_route_tables[0]['RouteTableId']
        print(f"! Route table exists for {VPC_NAME}")
        return route_table_id
    else:
        print(f"No route tables found for {VPC_NAME}")
        return False

def create_route_table(vpc_id: str):
    response_existence = check_route_table_existence(vpc_id)
    if(response_existence):
        return response_existence
    else:
        print(f"! No route tables found for {VPC_NAME}, Do create One")
        response_route_table_creation = ec2.create_route_table(
            TagSpecifications=[
                {
                    'ResourceType': "route-table",
                    'Tags':[
                        {
                            'Key': 'boto3-ec2',
                            'Value':'foo-bar'
                        }
                    ]
                }
            ],
            VpcId=vpc_id
        )
        print(response_route_table_creation)