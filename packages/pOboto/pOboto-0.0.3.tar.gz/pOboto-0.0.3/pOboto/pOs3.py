import boto3
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

resource = boto3.resource('s3')


def object_put(bucket_name, bucket_path, ready_data, tags):
    resource.Object(bucket_name, bucket_path).put(
        Body=ready_data,
        Tagging=tags
    )


client = boto3.client('s3')


def copy_object(src_bucket, src_prefix, dest_bucket, dest_prefix):
    src_copy_to = src_bucket + '/' + src_prefix
    response = client.copy_object(
        Bucket=dest_bucket,
        CopySource=src_copy_to,
        Key=dest_prefix,
    )
    if 'errorMessage' in response:
        logging.error('aws s3 client copy_objects response: %s', response)
    else:
        logging.warning('aws s3 client copy_objects response: %s', response)


def list_objects(bucket, prefix):
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'errorMessage' in response:
        logging.error('aws s3 client list_objects response: %s', response)
    else:
        logging.warning('aws s3 client list_objects response: %s', response)
        if 'Contents' in response:
            return response['Contents']
    return


def delete_object(bucket, key):
    response = client.delete_object(Bucket=bucket, Key=key)
    if 'errorMessage' in response:
        logging.error('aws s3 client delete_object response: %s', response)
    else:
        logging.warning('aws s3 client delete_object response: %s', response)


def delete_object_recursively(bucket, prefix):
    contents = list_objects(bucket=bucket, prefix=prefix)
    for content in contents:
        if 'Key' in content:
            print('Deleting', content['Key'])
            delete_object(bucket=bucket, key=content['Key'])


def move_object_recursively(src_bucket, src_prefix, dest_bucket):
    contents = list_objects(bucket=src_bucket, prefix=src_prefix)
    for content in contents:
        if 'Key' in content:
            copy_object(src_bucket, content['Key'], dest_bucket, content['Key'])
    delete_object_recursively(bucket=src_bucket, prefix=src_prefix)

