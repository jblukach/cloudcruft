import asyncio
import json
import whodap

def handler(event, context):

    print(event)

    getpath = event['rawPath'][1:]
    domain = getpath.split('.')
    
    if len(domain) > 1:

        try:

            response = whodap.lookup_domain(domain=domain[-2], tld=domain[-1])
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(whodap.aio_lookup_domain(domain=domain[-2], tld=domain[-1]))
            msg = response.to_dict()
            code = 200

        except:
            code = 200
            msg = 'Where the Internet Ends'
            pass

    else:
        code = 404
        msg = 'Where the Internet Ends'

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }