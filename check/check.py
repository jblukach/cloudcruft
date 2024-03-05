def handler(event, context):

    keys = event['event']['keys']

    if len(keys) > 0:
        status = 'CONTINUE'
    else:
        status = 'SUCCEEDED'
        print('NO KEYS LEFT')

    getobject = {}
    getobject['keys'] = keys

    return {
        'event': getobject,
        'status': status,
    }