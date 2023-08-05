import boto3

cloudwatch = boto3.client('cloudwatch')


def put_metric(namespace, metric_name, dimension_name, dimension_value, units, value):
    response = False
    try:
        response = cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': [
                        {
                            'Name': dimension_name,
                            'Value': dimension_value
                        },
                    ],
                    'Unit': units,
                    'Value': value
                },
            ],
            Namespace=namespace
        )
    except:
        # Log to file
        print('CloudWatch PutMetric Failed')

    return response
