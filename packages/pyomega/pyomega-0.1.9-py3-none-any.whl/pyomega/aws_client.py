import os
import boto3

class AWSClient:

    def __init__(self):
        self._aws_region = os.environ["AWS_REGION"]
        self._aws_access_key = os.environ["AWS_ACCESS_KEY_ID"]
        self._aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]

    def client(self, service):
        if "LOCAL" in os.environ:
            return boto3.client(service, region_name=self._aws_region,
                                aws_access_key_id=self._aws_access_key,
                                aws_secret_access_key=self._aws_secret_key)
        return boto3.client(service)

    def resource(self, service):
        if "LOCAL" in os.environ:
            return boto3.resource(service, region_name=self._aws_region,
                                  aws_access_key_id=self._aws_access_key,
                                  aws_secret_access_key=self._aws_secret_key)
        return boto3.resource(service)