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

    status = ssm.get_parameter(
        Name = os.environ['STATUS_PARAMETER_IPV4'],
        WithDecryption = False
    )

    sha256 = hasher('/tmp/ipv4.parquet')

    if status['Parameter']['Value'] != sha256:

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28'
        }

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        data = '''{
            "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(epoch)+'''",
            "target_commitish":"main",
            "name":"cloudcruft-ipv4",
            "body":"The sha256 verification hash for the ipv4.parquet file is: '''+sha256+'''",
            "draft":false,
            "prerelease":false,
            "generate_release_notes":false
        }'''

        response = requests.post(
            'https://api.github.com/repos/jblukach/cloudcruft/releases',
            headers=headers,
            data=data
        )

        print(response.json())

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/octet-stream'
        }

        params = {
            "name":"ipv4.parquet"
        }

        url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(response.json()['id'])+'/assets'

        with open('/tmp/ipv4.parquet', 'rb') as f:
            data = f.read()
        f.close()

        response = requests.post(url, params=params, headers=headers, data=data)

        print(response.json())

        ssm.put_parameter(
            Name = os.environ['STATUS_PARAMETER_IPV4'],
            Description = 'CloudCruft IPv4 Status',
            Value = sha256,
            Type = 'String',
            Overwrite = True
        )

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

    status = ssm.get_parameter(
        Name = os.environ['STATUS_PARAMETER_IPV6'],
        WithDecryption = False
    )

    sha256 = hasher('/tmp/ipv6.parquet')

    if status['Parameter']['Value'] != sha256:

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28'
        }

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        data = '''{
            "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(epoch)+'''",
            "target_commitish":"main",
            "name":"cloudcruft-ipv6",
            "body":"The sha256 verification hash for the ipv6.parquet file is: '''+sha256+'''",
            "draft":false,
            "prerelease":false,
            "generate_release_notes":false
        }'''

        response = requests.post(
            'https://api.github.com/repos/jblukach/cloudcruft/releases',
            headers=headers,
            data=data
        )

        print(response.json())

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/octet-stream'
        }

        params = {
            "name":"ipv6.parquet"
        }

        url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(response.json()['id'])+'/assets'

        with open('/tmp/ipv6.parquet', 'rb') as f:
            data = f.read()
        f.close()

        response = requests.post(url, params=params, headers=headers, data=data)

        print(response.json())

        ssm.put_parameter(
            Name = os.environ['STATUS_PARAMETER_IPV6'],
            Description = 'CloudCruft IPv6 Status',
            Value = sha256,
            Type = 'String',
            Overwrite = True
        )

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

    status = ssm.get_parameter(
        Name = os.environ['STATUS_PARAMETER_DNS'],
        WithDecryption = False
    )

    sha256 = hasher('/tmp/dns.parquet')

    if status['Parameter']['Value'] != sha256:

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28'
        }

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        data = '''{
            "tag_name":"v'''+str(year)+'''.'''+str(month)+'''.'''+str(epoch)+'''",
            "target_commitish":"main",
            "name":"cloudcruft-dns",
            "body":"The sha256 verification hash for the dns.parquet file is: '''+sha256+'''",
            "draft":false,
            "prerelease":false,
            "generate_release_notes":false
        }'''

        response = requests.post(
            'https://api.github.com/repos/jblukach/cloudcruft/releases',
            headers=headers,
            data=data
        )

        print(response.json())

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/octet-stream'
        }

        params = {
            "name":"dns.parquet"
        }

        url = 'https://uploads.github.com/repos/jblukach/cloudcruft/releases/'+str(response.json()['id'])+'/assets'

        with open('/tmp/dns.parquet', 'rb') as f:
            data = f.read()
        f.close()

        response = requests.post(url, params=params, headers=headers, data=data)

        print(response.json())

        ssm.put_parameter(
            Name = os.environ['STATUS_PARAMETER_DNS'],
            Description = 'CloudCruft DNS Status',
            Value = sha256,
            Type = 'String',
            Overwrite = True
        )

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