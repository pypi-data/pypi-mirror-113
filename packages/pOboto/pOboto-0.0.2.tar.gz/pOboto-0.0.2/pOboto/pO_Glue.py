import boto3
import logging

client = boto3.client('glue')


def batch_delete_table(CatalogId=None, DatabaseName=None, TablesToDelete=None):
    if CatalogId is None:
        response = client.batch_delete_table(
            DatabaseName=DatabaseName,
            TablesToDelete=TablesToDelete
        )
    else:
        response = client.batch_delete_table(
            CatalogId=CatalogId,
            DatabaseName=DatabaseName,
            TablesToDelete=TablesToDelete
        )
    if 'errorMessage' in response:
        logging.error('aws glue client response: %s', response)
    else:
        logging.warning('aws glue client response: %s', response)


def reset_job_bookmark(JobName=None, RunId=None):
    if RunId is None:
        response = client.reset_job_bookmark(
            JobName=JobName
        )
    else:
        response = client.reset_job_bookmark(
            JobName=JobName,
            RunId=RunId
        )

    if 'errorMessage' in response:
        logging.error('aws glue client response: %s', response)
    else:
        logging.warning('aws glue client response: %s', response)


