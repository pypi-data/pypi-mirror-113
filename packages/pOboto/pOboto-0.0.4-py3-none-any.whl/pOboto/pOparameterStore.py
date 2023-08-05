import boto3
import botocore
from botocore.exceptions import ClientError

ssm = boto3.client('ssm', region_name='us-east-1')


def get_parameter(param_name):
    try:
        response = ssm.get_parameter(
            Name=param_name,
            WithDecryption=True
        )
        param_value = response['Parameter']['Value']
    except ClientError as e:
        raise e

    return param_value


def put_parameter(param_name, param_value, param_description):
    try:
        response = ssm.put_parameter(
            Name=param_name,
            Description=param_description,
            Value=param_value,
            Type='String',
            Overwrite=True
        )
    except ClientError as e:
        raise e
    return response
