# s3_io.py
import json
import boto3
from botocore.exceptions import ClientError

_s3 = boto3.client("s3")

def load_json(bucket: str, key: str, default):
    try:
        obj = _s3.get_object(Bucket=bucket, Key=key)
        return json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("NoSuchKey", "NoSuchBucket"):
            return default
        raise

def save_json(bucket: str, key: str, data):
    body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    _s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return f"s3://{bucket}/{key}"
