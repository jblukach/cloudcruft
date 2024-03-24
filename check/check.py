import boto3
import datetime
import json
from boto3.dynamodb.conditions import Key

def handler(event, context):

    keys = event['event']['keys']
    total = event['event']['total']

    if len(keys) > 0:
        status = 'CONTINUE'
    else:
        status = 'SUCCEEDED'

        dynamodb = boto3.resource('dynamodb')
        feed = dynamodb.Table('feed')

        output = {}
        output['name'] = 'Cloud Cruft'
        output['description'] = 'Threat Feed for Cloud/SaaS Providers'
        output['created'] = str(datetime.datetime.now())
        output['epoch'] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        output['source'] = 'https://feed.tundralabs.net'

        response = feed.query(
            KeyConditionExpression=Key('pk').eq('IP#')
        )
        responsedata = response['Items']
        while 'LastEvaluatedKey' in response:
            response = feed.query(
                KeyConditionExpression=Key('pk').eq('IP#'),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            responsedata.extend(response['Items'])

        output['count'] = len(responsedata)
        output['reputation'] = []

        for item in responsedata:
            temp = {}
            temp['ip'] = item['ip']
            temp['source'] = item['source']
            temp['provider'] = item['provider']
            temp['last'] = item['last']
            temp['epoch'] = int(item['epoch'])
            output['reputation'].append(temp)

        f = open('/tmp/cloudcruft.json','w')
        f.write(json.dumps(output, indent = 4))
        f.close()

        s3 = boto3.resource('s3')

        s3.meta.client.upload_file(
            '/tmp/cloudcruft.json',
            'feed.tundralabs.net',
            'cloudcruft.json',
            ExtraArgs = {
                'ContentType': "application/json"
            }
        )

    getobject = {}
    getobject['keys'] = keys
    getobject['total'] = total

    return {
        'event': getobject,
        'status': status,
    }