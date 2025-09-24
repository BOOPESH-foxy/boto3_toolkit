import os
import typer
from vpc import setup_ec2_resources
from ssh_ec2 import ssh_ec2_instance
from key_pair import check_key_pair,key_pair_generation
from ec2_instance import check_instance_existence,create_ec2_instance,stop_ec2_instance,terminate_ec2_instance,start_ec2_instance


app = typer.Typer(help="EC2 CLI resource manager\n")

@app.command("check_key_pair")
def check_key_pair_typer():
    "Check if the mentioned (.env) key pair exists"
    check_key_pair()

@app.command("create_key_pair")
def create_key_pair_typer():
    "Creates key pair if the key-pair file mentioned in .env doesn't exist"
    key_pair_generation()

@app.command("create_ec2_instance")
def create_ec2_instance_typer():
    "Creates a complete ready to use ec2 instance with the .env parameters"
    create_ec2_instance()

@app.command("is_instance_running")
def check_instance_running_typer():
    "Checks if the instance provided in the .env is running "
    check_instance_existence()

@app.command("create_ec2_resources")
def create_ec2_resources_typer():
    "Creates and configures only the ec2 dependent resources such as VPC,igw,sg,subnets,route table"
    setup_ec2_resources()

@app.command("ssh_instance")
def ssh_instance_typer():
    "SSH into the created ec2 instance"
    ssh_ec2_instance()

@app.command("start_instance")
def stop_instance_typer():
    "Start the stopped ec2 instance"
    start_ec2_instance()

@app.command("stop_instance")
def stop_instance_typer():
    "Stop the ec2 instance"
    stop_ec2_instance()

@app.command("terminate_instance")
def terminate_instance_typer():
    "Terminate the ec2 instance"
    terminate_ec2_instance()


# TODO
# @app.command("delete_ec2_resources")
# def delete_instance_resources_typer():
#     "Deletes the VPC and attached resources(sg,igw,route-table,subnets)"
#     delete_ec2_resources()

if __name__ == "__main__":
    # os.system('clear')
    app()

