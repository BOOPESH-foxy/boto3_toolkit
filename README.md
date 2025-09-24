# AWS Boto3 Toolkit

A **ready-to-use Python toolkit built on boto3** that helps automate and manage **AWS resources** directly from the command line.  
This project is currently **enhanced for EC2** (VPCs, key pairs, security groups, subnets, and route tables), with initial support for **S3 bucket operations**.

The goal is to provide a **lightweight CLI toolkit** and reusable Python modules for everyday AWS automation tasks, perfect for **hands-on labs, experimentation, and learning**.

---

## Features

### EC2 (Enhanced & Tested)
- **VPC Management**: Create, describe, and verify VPCs by name, along with subnets and route tables.  
- **Key Pair Handling**: Generate and manage EC2 key pairs, store private keys locally, and set proper permissions.  
- **Security Groups**: Define and configure security groups for EC2 instances, including SSH access.  
- **EC2 Instance Management**: Launch, start, stop, and terminate EC2 instances programmatically.  
- **SSH Access via CLI**: Connect to instances interactively using Paramiko from the command line.  
- **Reusable EC2 Resource Client**: Wrapper around boto3 to simplify EC2 workflows.

### S3 (Work in Progress)
- **Bucket Operations**: List existing buckets, create new buckets via Typer CLI.  
- **S3 Client Wrapper**: Basic client setup to extend functionality in the future.

---

## Prerequisites

Before running the toolkit, install the following dependencies:

```bash
# AWS SDK for Python (EC2, S3, etc.)
pip install boto3

# Low-level AWS library for boto3 (auto-installed with boto3)
pip install botocore

# CLI framework for Python
pip install typer

# Load environment variables from .env files
pip install python-dotenv

# AWS CLI (optional, for broader command-line management)
pip install awscli
