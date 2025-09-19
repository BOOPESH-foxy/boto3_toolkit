import boto3
import os
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv('REGION')

def ec2_resource():
    return boto3.resource('ec2')

def ec2_client():
    return boto3.client('ec2',region_name=REGION)