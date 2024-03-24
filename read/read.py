import boto3
import datetime
import ipaddress
import json
import sqlite3

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    total = event['event']['total']
    keys = event['event']['keys']
    key = keys[0].split('/')
    source = key[1][:-4]

    s3 = boto3.client('s3')
    s3.download_file('projectcaretaker', keys[0], '/tmp/'+key[1])
    s3.download_file('static.tundralabs.net', 'distillery.sqlite3', '/tmp/distillery.sqlite3')

    with open('/tmp/'+key[1], 'r') as f:
        ips = f.readlines()
    f.close()

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    ttl = epoch+2592000 # plus 30 days
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    conn = sqlite3.connect('/tmp/distillery.sqlite3')
    dynamodb = boto3.resource('dynamodb')
    feed = dynamodb.Table('feed')

    if len(ips) <= total+1000:
        totals = len(ips)
    else:
        totals = total+1000

    for ip in ips[total:totals]:
        try:
            ip = ip[:-1]
            if ipaddress.ip_network(ip).version == 4:
                intip = int(ipaddress.IPv4Address(ip))
            else:
                intip = int(ipaddress.IPv6Address(ip))
            c = conn.cursor()
            c.execute("SELECT DISTINCT(source) FROM distillery WHERE firstip <= ? AND lastip >= ?", (str(intip), str(intip)))
            results = c.fetchall()
            if len(results) > 0:
                feed.put_item(
                    Item = {
                        'pk': 'IP#',
                        'sk': 'IP#'+str(ip)+'#SOURCE#'+source,
                        'ip': str(ip),
                        'provider': results,
                        'source': source,
                        'last': seen,
                        'epoch': epoch,
                        'ttl': ttl
                    }
                )
        except:
            pass

    conn.close()

    if len(ips) <= total+1000:
        keys.pop(0)
        totals = 0

    getobject = {}
    getobject['keys'] = keys
    getobject['total'] = totals

    return {
        'event': getobject,
        'status': 'CONTINUE',
    }