import boto3
import logging
import pOboto.pOsecretsManager as pOsecretsmanager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

client = boto3.client('redshift-data')


def execute_statement(cluster_identifier, database_name, secret_name, sql_string):
    response = pOsecretsmanager.get_secret_value(secret_name)
    secret_arn = response['ARN']
    response = client.execute_statement(
        ClusterIdentifier=cluster_identifier,
        Database=database_name,
        SecretArn=secret_arn,
        Sql=sql_string
    )
    return response


