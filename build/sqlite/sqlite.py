import boto3
import json
import os
import sqlite3
import zipfile

def handler(event, context):

    ### SQLITE ###

    if os.path.exists('/tmp/dns.sqlite3'):
        os.remove('/tmp/dns.sqlite3')

    db = sqlite3.connect('/tmp/dns.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS dns (pk INTEGER PRIMARY KEY, artifact TEXT, srcid TEXT)')
    db.execute('CREATE INDEX artifact_index ON dns (artifact)')
    db.execute('CREATE TABLE IF NOT EXISTS desc (pk INTEGER PRIMARY KEY, source TEXT)')

    ### DNS ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'dns'
    )

    for key in objects['Contents']:

        if key['Size'] != 0 and key['Key'] != 'dns.txt':

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            db.execute('INSERT INTO desc (source) VALUES (?)', (fname,))
            pkid = db.execute('SELECT pk FROM desc WHERE source = ?', (fname,)).fetchone()[0]

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n')

            for data in datas:
                if len(data) > 2:
                    db.execute('INSERT INTO dns (artifact, srcid) VALUES (?, ?)', (data, pkid))

    db.commit()
    db.close()

    ### UPLOAD ###

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/dns.sqlite3',
        os.environ['UL_BUCKET'],
        'dns.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    ### SQLITE ###

    if os.path.exists('/tmp/ipv4.sqlite3'):
        os.remove('/tmp/ipv4.sqlite3')

    db = sqlite3.connect('/tmp/ipv4.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS ipv4 (pk INTEGER PRIMARY KEY, artifact TEXT, srcid TEXT)')
    db.execute('CREATE INDEX artifact_index ON ipv4 (artifact)')
    db.execute('CREATE TABLE IF NOT EXISTS desc (pk INTEGER PRIMARY KEY, source TEXT)')

    ### IPv4 ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv4'
    )

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            db.execute('INSERT INTO desc (source) VALUES (?)', (fname,))
            pkid = db.execute('SELECT pk FROM desc WHERE source = ?', (fname,)).fetchone()[0]

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n')

            for data in datas:
                if len(data) > 2:
                    db.execute('INSERT INTO ipv4 (artifact, srcid) VALUES (?, ?)', (data, pkid))

    db.commit()
    db.close()

    ### UPLOAD ###

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/ipv4.sqlite3',
        os.environ['UL_BUCKET'],
        'ipv4.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    ### SQLITE ###

    if os.path.exists('/tmp/ipv6.sqlite3'):
        os.remove('/tmp/ipv6.sqlite3')

    db = sqlite3.connect('/tmp/ipv6.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS ipv6 (pk INTEGER PRIMARY KEY, artifact TEXT, srcid TEXT)')
    db.execute('CREATE INDEX artifact_index ON ipv6 (artifact)')
    db.execute('CREATE TABLE IF NOT EXISTS desc (pk INTEGER PRIMARY KEY, source TEXT)')

    ### IPv6 ###

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['DL_BUCKET'],
        Prefix = 'ipv6'
    )

    for key in objects['Contents']:

        if key['Size'] != 0:

            fname = key['Key'].split('/')[1]
            print(key['Key'])

            db.execute('INSERT INTO desc (source) VALUES (?)', (fname,))
            pkid = db.execute('SELECT pk FROM desc WHERE source = ?', (fname,)).fetchone()[0]

            s3.download_file(os.environ['DL_BUCKET'], key['Key'], '/tmp/'+fname)

            f = open('/tmp/'+fname, 'r')
            data = f.read()
            f.close()

            datas = data.split('\n')

            for data in datas:
                if len(data) > 2:
                    db.execute('INSERT INTO ipv6 (artifact, srcid) VALUES (?, ?)', (data, pkid))

    db.commit()
    db.close()

    ### UPLOAD ###

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/ipv6.sqlite3',
        os.environ['UL_BUCKET'],
        'ipv6.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    ### DEPLOYMENT ###

    s3 = boto3.client('s3')

    s3.download_file(
        os.environ['UL_BUCKET'],
        'dns.py',
        '/tmp/dns.py'
    )

    s3.download_file(
        os.environ['UL_BUCKET'],
        'ipv4.py',
        '/tmp/ipv4.py'
    )

    s3.download_file(
        os.environ['UL_BUCKET'],
        'ipv6.py',
        '/tmp/ipv6.py'
    )

    ### COMPRESSION ###

    with zipfile.ZipFile('/tmp/dns.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

        zipf.write(
            '/tmp/dns.py',
            'dns.py'
        )

        zipf.write(
            '/tmp/dns.sqlite3',
            'dns.sqlite3'
        )

    zipf.close()

    with zipfile.ZipFile('/tmp/ipv4.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

        zipf.write(
            '/tmp/ipv4.py',
            'ipv4.py'
        )

        zipf.write(
            '/tmp/ipv4.sqlite3',
            'ipv4.sqlite3'
        )

    zipf.close()

    with zipfile.ZipFile('/tmp/ipv6.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

        zipf.write(
            '/tmp/ipv6.py',
            'ipv6.py'
        )

        zipf.write(
            '/tmp/ipv6.sqlite3',
            'ipv6.sqlite3'
        )

    zipf.close()

    ### UPLOAD ZIP ###

    s3.upload_file(
        '/tmp/dns.zip',
        os.environ['UL_BUCKET'],
        'dns.zip'
    )

    s3.upload_file(
        '/tmp/ipv4.zip',
        os.environ['UL_BUCKET'],
        'ipv4.zip'
    )

    s3.upload_file(
        '/tmp/ipv6.zip',
        os.environ['UL_BUCKET'],
        'ipv6.zip'
    )

    ### UPDATE FUNCTION ###

    client = boto3.client('lambda')

    response = client.update_function_code(
        FunctionName = 'dns',
        S3Bucket = os.environ['UL_BUCKET'],
        S3Key = 'dns.zip'
    )

    response = client.update_function_code(
        FunctionName = 'ipv4',
        S3Bucket = os.environ['UL_BUCKET'],
        S3Key = 'ipv4.zip'
    )

    response = client.update_function_code(
        FunctionName = 'ipv6',
        S3Bucket = os.environ['UL_BUCKET'],
        S3Key = 'ipv6.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('SQLite Exported!')
    }