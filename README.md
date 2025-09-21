# AWS Boto3 Toolkit

A **Python toolkit built on boto3** that helps automate and manage **AWS resources** from the command line.  
This project is currently **enhanced for EC2** (VPC, key pairs, and security groups), with initial support for **S3 bucket operations**.

The goal is to provide a **lightweight CLI toolkit** and reusable Python modules for everyday AWS tasks.

---

## Features

### EC2 (Enhanced & Tested)
- **VPC Management**: Create, describe, and verify VPCs by name.
- **Key Pair Handling**: Create and manage EC2 key pairs.
- **Security Groups**: Define and configure security groups for your workloads.
- **EC2 Resource Client**: Wrapper around boto3 to simplify EC2 workflows.

### S3 (Work in Progress)
- **Bucket Operations**: List buckets, create new ones (via Typer CLI).
- **S3 Client Wrapper**: Basic client setup to extend later.

---

## Prerequisites

Before running the toolkit, you need to install the following dependencies:

```bash
# AWS SDK for Python (EC2, S3, etc.)
pip install boto3

# Low-level AWS library for boto3 (auto-installed with boto3)
pip install botocore

# For creating the CLI interface
pip install typer

# For loading environment variables from .env files
pip install python-dotenv

# AWS CLI (optional, for broader AWS command-line management)
pip install awscli

# HTTP requests needed by botocore and boto3
pip install requests
