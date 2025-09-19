import bucket_ops as bucket
import typer

app = typer.Typer(help="B3: your s3 CLI")

@app.command("list_buckets")

def list_buckets():
    "List of available Buckets"
    names = bucket.list_buckets()
    typer.echo(names)

@app.command("create_bucket")

def create_bucket(name,region):
    "Create new bucket"
    api_result = bucket.create_bucket(name,region)
    typer.echo(api_result)

if __name__ == "__main__":
    app()