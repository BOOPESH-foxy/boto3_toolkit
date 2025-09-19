import boto3

def s3_resource():
    return boto3.resource('s3')

def s3_client():
    return boto3.client('s3')