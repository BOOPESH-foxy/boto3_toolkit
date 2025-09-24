import os
import botocore
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
        route_table_id = create_route_table()
        return route_table_id

def create_route_table(vpc_id: str):
    try:
        print(f"Creating route table for {VPC_NAME}")
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
    except botocore.Exception as e:
        print(":: Error ::",e)
        raise

def modify_route_table():
    route_table_id = check_route_table_existence()