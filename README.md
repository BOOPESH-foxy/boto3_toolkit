# AWS EC2 Automation with Boto3

This repository is a **hands-on tutorial** for managing **Amazon EC2** instances using **Python (boto3)**.  
It is structured step by step: starting from **key pair generation**, and extending toward **security groups, launching instances, and SSH connections**.

---

## Roadmap

- Generate and manage EC2 key pairs  
- Create and manage security groups (firewall rules)  
- Launch EC2 instances  
- Wait for instance readiness  
- SSH into EC2 instances and run commands  
- Interactive shell access via Python  

---

## Setup

### 1. Install and configure
```bash
pip install boto3 python-dotenv
aws configure
```
### 2. .env
- create a .env file with the following contents
  ```env
    REGION = 'your-aws-region'
    KEY_NAME = 'your-user-key'
    KEY_FILE = '../path-to/generated-key-pair.pem'
    INSTANCE_TYPE = 'desired-instance-type'
    CIDR_BLOCK = 'desired-ip/16'


### 3. Clone repo and start execution
```bash
git clone https://github.com/BOOPESH-foxy/boto3_toolkit.git
cd boto3_toolkit/ec2
python3 main.py
```

## Learning Goals
1. Work with EC2 key pairs
2. Understand security groups and why they matter
3. Launch and manage EC2 instances with Python
4. Connect to EC2 programmatically and securely

## Notes
1. Never commit your .pem files
2. AWS will only give the private key once. If lost, delete and recreate the key pair.
3. Allow SSH access only to the required IP's(Avoid 0.0.0.0/0).

## Contributions

Contributions are welcome! Fork the repo, open issues, or submit PRs to expand EC2 automation (EBS volumes, snapshots, AMI management, etc.).