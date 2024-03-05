import boto3
import json

def handler(event, context):

    parameter = boto3.client('ssm')

    ssm = parameter.get_parameter(
        Name = '/tacklebox/cloudcruft'
    )

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = 'projectcaretaker',
        Prefix = 'ip'
    )

    keys = []
    for key in objects['Contents']:
        keys.append(key['Key'])

    getobject = {}
    getobject['keys'] = keys

    step = boto3.client('stepfunctions')
     
    step.start_execution(
        stateMachineArn = ssm['Parameter']['Value'],
        input = json.dumps(getobject)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Start Cloud Cruft!')
    }