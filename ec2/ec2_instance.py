import os
import vpc
import botocore
from dotenv import load_dotenv
from ec2_resource import ec2_client

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
    print(f"\n! Fetching AMI id for {os_choise['name']}")
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

def check_stopped_instance_existence():
    print(f"! Checking for stopped {INSTANCE_NAME} existence")
    response_instance_existence = ec2.describe_instances(
        Filters=[{
            'Name':'tag:Name','Values':[INSTANCE_NAME],
            'Name':'instance-state-name','Values':['stopped'],
        }]
    )
    images = response_instance_existence['Reservations']
    if(images):
        images_data = images[0]['Instances']
        instanceId = images_data[0]['InstanceId']
        print(f"! Instance {INSTANCE_NAME} exists.")
        return instanceId
    else:
        print(f"! Instance {INSTANCE_NAME} doesnt exists.")
        return False

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
        print("! Instance is running with the given name !")
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
            vpc_setup_results = vpc.setup_ec2_resources()
            subnet_id = vpc_setup_results['subnet_id']
            sg_id = vpc_setup_results['sg_id']

            response_run_instances = ec2.run_instances(
                ImageId=get_ami_id('1'),
                InstanceType=INSTANCE_TYPE,
                MaxCount=1,
                MinCount=1,
                KeyName=KEY_NAME,
                NetworkInterfaces=[{
                    'SubnetId': subnet_id,
                    'DeviceIndex': 0,
                    'Groups': [sg_id],
                    'AssociatePublicIpAddress': True
                }],
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': INSTANCE_NAME}]
                }]
            )
            instance_id=response_run_instances['Instances'][0]
            id=instance_id['InstanceId']
            wait_for = 'instance_running'
            wait_for_instance_state(id,wait_for)
            print(f"+ Created instance {INSTANCE_NAME} id={id}")
            return id
        
        except botocore.exceptions.ClientError as e:
            print(":: Error :",e)
            raise

def wait_for_instance_state(id: str,wait_for: str):
    waiter = ec2.get_waiter(wait_for)
    waiter.wait(InstanceIds=[id])

def start_ec2_instance():
    instance_id = check_stopped_instance_existence()
    if(instance_id):
        print(f"! To Start a stopped instance {INSTANCE_NAME}")
        response = ec2.start_instances(
            InstanceIds=[instance_id]
        )
        wait_for = 'instance_running'
        wait_for_instance_state(instance_id,wait_for)
        print("- Started instance successfully")
        return True

def stop_ec2_instance():
    instance_id = check_instance_existence()
    if(instance_id):
        print(f"! To Stop instance {INSTANCE_NAME}")
        response = ec2.stop_instances(
            InstanceIds=[instance_id]
        )
        wait_for = 'instance_stopped'
        wait_for_instance_state(instance_id,wait_for)
        print("- Stopped instance successfully")
        return True

def terminate_ec2_instance():
    instance_id = check_stopped_instance_existence()
    if(instance_id):
        print(f"! Terminating instance {INSTANCE_NAME}")
        response = ec2.terminate_instances(
            InstanceIds=[instance_id]
        )
        wait_for = 'instance_terminated'
        wait_for_instance_state(instance_id,wait_for)
        print("- Terminated instance successfully")
        return True

def get_public_ip():
    print(f"! Getting public ip for {INSTANCE_NAME}")
    response_public_ip = ec2.describe_instances(
        Filters=[{
            'Name':'tag:Name','Values':[INSTANCE_NAME],
            'Name':'instance-state-name','Values':['running'],
        }]
    )
    images = response_public_ip['Reservations']
    if(images):
        images_data = images[0]['Instances']
        Associtaion_data = images_data[0]['NetworkInterfaces'][0]['Association']
        public_ip = Associtaion_data['PublicIp']
        print(public_ip)
        return public_ip
    else:
        print(f"! Instance {INSTANCE_NAME} doesnt exists.")
        return False
