from client import s3_resource

s3 =  s3_resource()

def list_buckets() -> list[str]:

    for bucket in s3.buckets.all():
        print(bucket.name)


def create_bucket(name: str, region: str = "ap-south-1"):
    if(region == ('ap-south-1')):
        print("default region")
        return s3.create_bucket(Bucket=name,CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    
    else:
        print("new region - ",region)
        return s3.create_bucket(Bucket=name,CreateBucketConfiguration={'LocationConstraint': region})