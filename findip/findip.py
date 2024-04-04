import boto3
import ipaddress
import json
import pandas as pd

def handler(event, context):

    print(event)

    try:

        getpath = event['rawPath'][1:]
        iptype = ipaddress.ip_address(event['rawPath'][1:])

        s3 = boto3.client('s3')
        s3.download_file('static.tundralabs.net', 'ip.parquet', '/tmp/ip.parquet')

        address = pd.read_parquet('/tmp/ip.parquet')
        address = address[address['address'].str.contains(getpath)]
        msg = json.loads(address.to_json())
        code = 200

    except:

        msg = 'Where the Internet Ends'
        code = 404

    return {
        'statusCode': 200,
        'body': json.dumps(msg, indent = 4)
    }