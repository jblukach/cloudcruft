import boto3
import json
import pandas as pd

def handler(event, context):

    print(event)

    try:

        getpath = event['rawPath'][1:]
        domain = getpath.split('.')

        if len(getpath) <= 2:

            msg = 'Where the Internet Ends'
            code = 404

        else:

            s3 = boto3.client('s3')
            s3.download_file('static.tundralabs.net', 'dns.parquet', '/tmp/dns.parquet')

            dns = pd.read_parquet('/tmp/dns.parquet')
            dns = dns[dns['domain'].str.contains(getpath)]
            msg = json.loads(dns.to_json())
            code = 200

    except:

        msg = 'Where the Internet Ends'
        code = 404

        pass

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }