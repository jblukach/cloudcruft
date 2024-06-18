import json
import sqlite3

def handler(event, context):

    print(event)

    try:

        code = 200
        dns = event['rawPath'][1:]
        domain = dns.split('.')
    
        if len(domain) > 1:

            conn = sqlite3.connect('dns.sqlite3')
            c = conn.cursor()
            c.execute("SELECT dns.artifact, desc.source FROM dns JOIN desc ON dns.srcid = desc.pk WHERE dns.artifact = ?", (dns,))
            msg = c.fetchall()
            conn.close()

        else:

            msg = 'Where the Internet Ends'

    except:

        msg = 'Where the Internet Ends'
        code = 404

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }