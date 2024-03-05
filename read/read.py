def handler(event, context):

    keys = event['event']['keys']

    # print first item in keys lilst
    print(keys[0])



    #remove first item in keys list
    keys.pop(0)

    getobject = {}
    getobject['keys'] = keys

    return {
        'event': getobject,
        'status': 'CONTINUE',
    }