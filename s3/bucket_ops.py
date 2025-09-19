from client import s3_resource

s3 =  s3_resource()

def list_buckets() -> list[str]:

    for bucket in s3.buckets.all():
        print(bucket.name)


def create_bucket(name: str, region: str = "ap-south-1"):
    raise NotImplementedError