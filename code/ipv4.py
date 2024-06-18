import ipaddress
import json
import sqlite3

def handler(event, context):

    print(event)

    try:

        code = 200
        msg = 'Where the Internet Ends'

        ip = event['rawPath'][1:]

        if ipaddress.ip_network(ip).version == 4:

            conn = sqlite3.connect('ipv4.sqlite3')
            c = conn.cursor()
            c.execute("SELECT ipv4.artifact, desc.source FROM ipv4 JOIN desc ON ipv4.srcid = desc.pk WHERE ipv4.artifact = ?", (ip,))
            msg = c.fetchall()
            conn.close()

    except:

        msg = 'Where the Internet Ends'
        code = 404

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }