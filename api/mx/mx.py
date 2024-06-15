import dns.resolver
import json

def handler(event, context):

    print(event)

    getpath = event['rawPath'][1:]
    domain = getpath.split('.')
    
    if len(domain) > 1:

        try:
            answers = dns.resolver.resolve(getpath, 'MX')
            mx_records = [str(rdata.exchange) for rdata in answers]
        except:
            mx_records = []
            pass

        try:
            spf_records = []
            txt_records = []
            answers = dns.resolver.resolve(getpath, 'TXT')
            for rdata in answers:
                if 'v=spf1' in str(rdata):
                    spf_records.append(str(rdata))
                else:
                    txt_records.append(str(rdata))
        except:
            spf_records = []
            txt_records = []
            pass
    
        try:
            answers = dns.resolver.resolve('_dmarc.' + getpath, 'TXT')
            dmarc_records = [str(rdata) for rdata in answers]
        except:
            dmarc_records = []
            pass

        dkim_records = []

        try:
            answers = dns.resolver.resolve('sig1._domainkey.' + getpath, 'CNAME')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        try:
            answers = dns.resolver.resolve('selector1._domainkey.' + getpath, 'TXT')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        try:
            answers = dns.resolver.resolve('selector1._domainkey.' + getpath, 'CNAME')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        try:
            answers = dns.resolver.resolve('google._domainkey.' + getpath, 'TXT')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        try:
            answers = dns.resolver.resolve('s1._domainkey.' + getpath, 'TXT')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        try:
            answers = dns.resolver.resolve('s1._domainkey.' + getpath, 'CNAME')
            dkim_records = [str(answer) for answer in answers] + dkim_records
        except:
            pass

        code = 200
        msg = {
            'domain':getpath,
            'dkim':dkim_records,
            'dmarc':dmarc_records,
            'mx':mx_records,
            'spf':spf_records,
            'txt':txt_records,
            
        }

    else:
        code = 404
        msg = 'Where the Internet Ends'

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }