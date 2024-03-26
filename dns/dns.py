import boto3
import datetime
import hashlib
import json
import os
import pandas as pd

def hasher(filename):
    
    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()

    with open(filename,'rb') as h:
        buf = h.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = h.read(BLOCKSIZE)
    h.close()

    sha256 = sha256_hasher.hexdigest().upper()

    return sha256

def handler(event, context):

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = 'projectcaretaker',
        Prefix = 'dns'
    )

    df = pd.DataFrame(columns=['domain', 'source'])

    for key in objects['Contents']:

        fname = key['Key'].split('/')[1]
        source = fname[:-4]
        print(key['Key'])

        s3.download_file('projectcaretaker', key['Key'], '/tmp/'+fname)

        temp = pd.read_csv('/tmp/'+fname, header=None)
        temp.columns = ['domain']
        temp['source'] = source

        df = pd.concat([df, temp], ignore_index=True)

    df.to_parquet('/tmp/dns.parquet', compression='gzip')

    source_count = df['source'].value_counts().reset_index()
    source_count.columns = ['source', 'count']

    f = open('/tmp/dns.sha256','w')
    f.write(hasher('/tmp/dns.parquet'))
    f.close()

    f = open('/tmp/dns.updated','w')
    f.write(str(datetime.datetime.now()))
    f.close()

    f = open('/tmp/dns.count','w')
    f.write(str(source_count))
    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/dns.parquet',
        os.environ['UP_BUCKET'],
        'dns.parquet',
        ExtraArgs = {
            'ContentType': "application/vnd.apache.parquet"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/dns.sha256',
        os.environ['UP_BUCKET'],
        'dns.sha256',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/dns.updated',
        os.environ['UP_BUCKET'],
        'dns.updated',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/dns.count',
        os.environ['UP_BUCKET'],
        'dns.count',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Build DNS')
    }