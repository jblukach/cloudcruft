import boto3
import json
import os
import zipfile

def handler(event, context):

    ### DNS ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'dns'
    )

    datas = []

    for key in objects['Contents']:

        if key['Size'] != 0 and key['Key'] != 'dns.txt':

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n') + datas

    datas = list(set(datas))
    print('DNS: '+str(len(datas)))

    f = open('/tmp/dns.txt','w')

    for data in datas:
        if len(data) > 2:
            f.write(data+'\n')

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/dns.txt',
        os.environ['UL_BUCKET'],
        'dns.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    ### IPv4 ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv4'
    )

    datas = []

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n') + datas

    datas = list(set(datas))
    print('IPv4: '+str(len(datas)))

    f = open('/tmp/ipv4.txt','w')

    for data in datas:
        if len(data) > 2:
            f.write(data+'\n')

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/ipv4.txt',
        os.environ['UL_BUCKET'],
        'ipv4.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    ### IPv6 ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv6'
    )

    datas = []

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n') + datas

    datas = list(set(datas))
    print('IPv6: '+str(len(datas)))

    f = open('/tmp/ipv6.txt','w')

    for data in datas:
        if len(data) > 2:
            f.write(data+'\n')

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/ipv6.txt',
        os.environ['UL_BUCKET'],
        'ipv6.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    ### DELPLOYMENT ###

    s3 = boto3.client('s3')

    s3.download_file(
        os.environ['UL_BUCKET'],
        'spf.py',
        '/tmp/spf.py'
    )

    with zipfile.ZipFile('/tmp/spf.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

        zipf.write(
            '/tmp/spf.py',
            'spf.py'
        )

        zipf.write(
            '/tmp/dns.txt',
            'dns.txt'
        )

        zipf.write(
            '/tmp/ipv4.txt',
            'ipv4.txt'
        )

        zipf.write(
            '/tmp/ipv6.txt',
            'ipv6.txt'
        )

    zipf.close()

    s3.upload_file(
        '/tmp/spf.zip',
        os.environ['UL_BUCKET'],
        'spf.zip'
    )

    client = boto3.client('lambda')

    response = client.update_function_code(
        FunctionName = 'spf',
        S3Bucket = os.environ['UL_BUCKET'],
        S3Key = 'spf.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Unique Exported!')
    }