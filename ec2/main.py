from key_pair import check_key_pair,key_pair_generation
from ec2_instance import check_instance_existence,create_ec2_instance
import typer
import os

app = typer.Typer(help="EC2 CLI resource manager")

@app.command("check_key_pair")
def check_key_pair_typer():
    """Check if the key pair exists"""
    check_key_pair()

@app.command("create_key_pair")
def create_key_pair_typer():
    "creates key pair if the key-pair file mentioned in .env doesn't exist"
    key_pair_generation()

@app.command("create_ec2_instance")
def create_ec2_instance_typer():
    "creates a complete ready to use ec2 instance with the .env parameters"
    create_ec2_instance()

@app.command("is_instance_running")
def check_instance_running_typer():
    "checks if the instance provided in the .env is running "
    check_instance_existence()

if __name__ == "__main__":
    os.system('clear')
    app()

