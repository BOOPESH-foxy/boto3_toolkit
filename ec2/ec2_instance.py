from ec2_resource import ec2_client
import vpc

ec2 = ec2_client()


OS_OPTIONS = {
"1": {"name": "Amazon Linux 2", "filter_name": "amzn2-ami-hvm-*-x86_64-gp2", "owner": "amazon"},
}


def get_ami_id(os_choise_num: str):
    os_choise = OS_OPTIONS[os_choise_num]
    os_id_filter = os_choise["filter_name"]
    print(os_id_filter)
    response_instances = ec2.describe_images(
        Owners=['amazon'],
        Filters=[
        {"Name": "name", "Values": [os_id_filter]},
        {"Name": "state", "Values": ["available"]}
        ]
    )
    images = response_instances['Images'][0]
    image_id = images['ImageId']
    print(image_id)

def create_ec2_instaces():
    pass
