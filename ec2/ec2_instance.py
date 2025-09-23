import os
import vpc
from ec2_resource import ec2_client
from dotenv import load_dotenv
import botocore

load_dotenv()
INSTANCE_TYPE=os.getenv('INSTANCE_TYPE')
KEY_NAME = os.getenv('KEY_NAME')
INSTANCE_NAME=os.getenv('INSTANCE_NAME')
ec2 = ec2_client()

OS_OPTIONS = {
"1": {"name": "Amazon Linux 2", "filter_name": "amzn2-ami-hvm-*-x86_64-gp2", "owner": "amazon"},
}

def get_ami_id(os_choise_num: str):
    os_choise = OS_OPTIONS[os_choise_num]
    print(f"! Fetching AMI id for {os_choise['name']}")
    os_id_filter = os_choise["filter_name"]
    response_instances = ec2.describe_images(
        Owners=['amazon'],
        Filters=[
        {"Name": "name", "Values": [os_id_filter]},
        {"Name": "state", "Values": ["available"]}
        ]
    )
    images = response_instances['Images'][0]
    image_id = images['ImageId']
    return image_id

def check_instance_existence():
    print(f"! Checking for {INSTANCE_NAME} existence")
    response_instance_existence = ec2.describe_instances(
        Filters=[{
            'Name':'tag:Name','Values':[INSTANCE_NAME],
            'Name':'instance-state-name','Values':['running'],
        }]
    )
    images = response_instance_existence['Reservations']
    if(images):
        images_data = images[0]['Instances']
        instanceId = images_data[0]['InstanceId']
        print("! Instance is already up with the given name !")
        return instanceId
    else:
        print(f"! Instance {INSTANCE_NAME} doesnt exists.")
        return False

def create_ec2_instance():
    response_check_instance_existence = check_instance_existence()
    if(response_check_instance_existence):
        return 0
    else:
        try:
            print("\n! Creating an EC2 instance")
            print("! Setting Up VPC resource\n")
            vpc_setup_results = vpc.setup_vpc_resources()
            subnet_id = vpc_setup_results['subnet_id']
            sg_id = vpc_setup_results['sg_id']

            response_run_instances = ec2.run_instances(
                ImageId=get_ami_id('1'),
                InstanceType=INSTANCE_TYPE,
                MaxCount=1,
                MinCount=1,
                KeyName=KEY_NAME,
                SubnetId=subnet_id,
                SecurityGroupIds=[sg_id],
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}]
                }]
            )
            instance_id=response_run_instances['Instances'][0]
            id=instance_id['InstanceId']
            wait_for_instance_creation(id)
            print(f"+ Created instance {INSTANCE_NAME} id={id}")
            return id
        
        except botocore.exceptions.ClientError as e:
            print(":: Error :",e)
            raise

def wait_for_instance_creation(id: str):
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[id])
