
# AWS EC2 Automation with Boto3

This repository is a **hands-on tutorial** for managing **Amazon EC2** instances using **Python (boto3)**.  
It is structured step by step, starting from **key pair generation**, and extending toward **security groups**, **VPC creation**, **subnet management**, **EC2 instance launching**, and more.

---

## Roadmap

- **Generate and manage EC2 key pairs**: Securely create and store key pairs for SSH access to EC2 instances.
- **Create and manage security groups**: Define firewall rules and security groups for EC2 instances.
- **Create VPC**: Create a Virtual Private Cloud (VPC) to launch resources in a secure and isolated network.
- **Create and manage subnets**: Define subnets in different Availability Zones (AZs) within your VPC.
- **Launch EC2 instances**: Provision EC2 instances using different configurations (e.g., instance types, AMIs, key pairs, etc.).
- **Configure Internet Gateway (IGW)**: Attach an Internet Gateway to the VPC for internet access.
- **SSH into EC2 instances**: Programmatically SSH into instances for configuration or application management.
- **Interactive shell access**: Connect to the instance’s shell and run commands from Python.

---

## Setup

### 1. Install and Configure
First, install the required dependencies:

```bash
pip install boto3 python-dotenv
```

Next, configure your AWS CLI with your credentials:

```bash
aws configure
```

This will prompt you for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format

### 2. .env File
Create a `.env` file with the following contents. This file will store your configuration securely.

```env
REGION = 'your-aws-region'  # Example: 'ap-south-1'
KEY_NAME = 'your-key-name'   # Example: 'my-ec2-key-pair'
KEY_FILE = '../path-to-generated-key-pair.pem'  # Path to save your private key or existing key
INSTANCE_TYPE = 't2.micro'  # Example: 't2.micro'
CIDR_BLOCK = '10.0.0.0/16'  # Example: VPC CIDR block
VPC_NAME = 'my-vpc'         # Name for your VPC
SECURITY_GROUP_NAME = 'my-security-group'  # Name for the security group
SUBNET_CIDR_BLOCK = '10.0.1.0/24'  # CIDR block for your subnet
```

**Important Notes**:
- **Never commit your private key (`.pem`) files** to the repository.
- AWS will only give the private key once. If lost, you will need to delete and recreate the key pair.

### 3. Clone the Repo and Start Execution
Clone this repository and navigate to the EC2 automation directory:

```bash
git clone https://github.com/your-repo/boto3_toolkit.git
cd boto3_toolkit/ec2
python3 main.py
```

---

## File Structure

Here’s a breakdown of the project’s file structure:

```
boto3_toolkit/
└── ec2/
    ├── ec2_instance.py      # EC2 instance creation and management
    ├── ec2_resource.py      # EC2 client and resource functions
    ├── key_pair.py          # EC2 key pair creation and management
    ├── vpc.py               # VPC creation, security groups, subnets, and IGW
    ├── route_table.py       # Route table creation and management
    ├── main.py              # Main script to run the EC2 and VPC automation
    ├── README.md               
    └── __pycache__/         # Compiled Python files (automatically generated)

```

### Module Descriptions:

- **`ec2_instance.py`**: This file contains functions for managing EC2 instances, including starting, stopping, and describing instances.
- **`ec2_resource.py`**: This provides functions for interacting with EC2 resources using the `boto3.resource` and `boto3.client` APIs.
- **`key_pair.py`**: This file handles key pair generation and checking if the key pair already exists in local path. It also manages storing the private key in a file and change its permissions using chmod.
- **`vpc.py`**: Manages the creation of VPCs, subnets, security groups, and internet gateways. It checks whether resources already exist and creates them if it doesn't exists.
- **`route_table.py`**: Manages creating and associating route tables with subnets in the VPC for traffic routing.
- **`main.py`**: The entry point of the script. It ties together the different operations like creating VPCs, security groups, subnets, ,instances and accessing them via ssh.

---

## Learning Goals

1. **Work with EC2 Key Pairs**: Learn how to securely generate, store, and use EC2 key pairs.
2. **Understand Security Groups**: Learn how to create and manage security groups to define firewall rules for EC2 instances.
3. **Launch EC2 Instances**: Learn how to provision EC2 instances with the right configuration (instance type, AMI, security groups, etc.).
## TODO's
1. **Connect to EC2 Instances Programmatically**: Use Python to SSH into EC2 instances and run commands interactively.

---

## Notes

- **Security**: Always ensure that your `.pem` files (private keys) are never committed to source control. They should be kept in a secure, private location.
- **IAM Permissions**: Ensure that your AWS credentials have appropriate permissions to create and manage EC2, VPC, and other AWS resources.
- **SSH Access**: Limit SSH access to the necessary IP ranges to enhance security (avoid using `0.0.0.0/0` for public access).

---

## Contributions

Contributions are welcome! If you’d like to improve this project, please:
- Fork the repo.
- Open issues for bug fixes or improvements.
- Submit pull requests (PRs) to expand EC2 automation features (e.g., EBS volume management, snapshots, AMI creation, etc.).

---

## Roadmap for Future Enhancements

1. **VPC Peering**: Automate VPC peering connections between multiple VPCs.
2. **NAT Gateway Setup**: Add support for setting up a NAT Gateway for private subnet internet access.
3. **AMI Management**: Add functionality to create and manage Amazon Machine Images (AMIs) from instances.
4. **EBS Volumes**: Add support for creating and attaching Elastic Block Store (EBS) volumes to EC2 instances.

---

Feel free to explore and add your own functionality to this automation toolkit. If you run into any issues or have questions, don’t hesitate to open an issue or reach out.
