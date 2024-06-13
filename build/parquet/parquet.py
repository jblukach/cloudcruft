import boto3
import datetime
import hashlib
import json
import os
import requests
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
    ssm = boto3.client('ssm')

    token = ssm.get_parameter(
        Name = os.environ['SSM_PARAMETER_GIT'], 
        WithDecryption = True
    )

    ### IPv4 ###

    df = pd.DataFrame(columns=['address', 'source'])

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv4'
    )

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            source = fname[:-4]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            temp = pd.read_csv('/tmp/'+fname, header=None)
            temp.columns = ['address']
            temp['source'] = source

            df = pd.concat([df, temp], ignore_index=True)

    df.to_parquet('/tmp/ipv4.parquet', compression='gzip')
    sha256ipv4 = hasher('/tmp/ipv4.parquet')

    ### IPv6 ###

    df = pd.DataFrame(columns=['address', 'source'])

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv6'
    )

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            source = fname[:-4]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            temp = pd.read_csv('/tmp/'+fname, header=None)
            temp.columns = ['address']
            temp['source'] = source

            df = pd.concat([df, temp], ignore_index=True)

    df.to_parquet('/tmp/ipv6.parquet', compression='gzip')
    sha256ipv6 = hasher('/tmp/ipv6.parquet')

    ### DNS ###

    df = pd.DataFrame(columns=['domain', 'source'])

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'dns'
    )

    for key in objects['Contents']:

        if key['Size'] != 0 and key['Key'] != 'dns.txt':

            fname = key['Key'].split('/')[1]
            source = fname[:-4]
            print(key['Key'])

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            temp = pd.read_csv('/tmp/'+fname, header=None)
            temp.columns = ['domain']
            temp['source'] = source

            df = pd.concat([df, temp], ignore_index=True)

    df.to_parquet('/tmp/dns.parquet', compression='gzip')
    sha256dns = hasher('/tmp/dns.parquet')

    ### RELEASE TAG ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28'
    }

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    data = '''{
        "tag_name":"v'''+str(year)+'''.'''+str(month)+str(day)+'''.'''+str(epoch)+'''",
        "target_commitish":"main",
        "name":"cloudcruft",
        "body":"The sha256 verifications: dns.parquet '''+sha256dns+''', ipv4.parquet '''+sha256ipv4+''', and ipv6.parquet '''+sha256ipv6+'''",
        "draft":false,
        "prerelease":false,
        "generate_release_notes":false
    }'''

    response = requests.post(
        'https://api.github.com/repos/jblukach/cloudcruft/releases',
        headers=headers,
        data=data
    )

    tagged = response.json()['id']
    print(response.json())

    ### DNS UPLOAD ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"dns.parquet"
    }

    url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(tagged)+'/assets'

    with open('/tmp/dns.parquet', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    ### IPv4 UPLOAD ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"ipv4.parquet"
    }

    url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(tagged)+'/assets'

    with open('/tmp/ipv4.parquet', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    ### IPv6 UPLOAD ###

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer '+token['Parameter']['Value'],
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/octet-stream'
    }

    params = {
        "name":"ipv6.parquet"
    }

    url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(tagged)+'/assets'

    with open('/tmp/ipv6.parquet', 'rb') as f:
        data = f.read()
    f.close()

    response = requests.post(url, params=params, headers=headers, data=data)

    print(response.json())

    ### S3 UPLOAD ###

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/ipv4.parquet',
        os.environ['UL_BUCKET'],
        'ipv4.parquet',
        ExtraArgs = {
            'ContentType': "application/vnd.apache.parquet"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/ipv6.parquet',
        os.environ['UL_BUCKET'],
        'ipv6.parquet',
        ExtraArgs = {
            'ContentType': "application/vnd.apache.parquet"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/dns.parquet',
        os.environ['UL_BUCKET'],
        'dns.parquet',
        ExtraArgs = {
            'ContentType': "application/vnd.apache.parquet"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Parquet Exported!')
    }