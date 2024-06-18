#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudcruft.cloudcruft_dns import CloudcruftDns
from cloudcruft.cloudcruft_egress import CloudcruftEgress
from cloudcruft.cloudcruft_ipv4 import CloudcruftIpv4
from cloudcruft.cloudcruft_ipv6 import CloudcruftIpv6
from cloudcruft.cloudcruft_mx import CloudcruftMx
from cloudcruft.cloudcruft_rdap import CloudcruftRdap
from cloudcruft.cloudcruft_spf import CloudcruftSpf
from cloudcruft.cloudcruft_stack import CloudcruftStack

app = cdk.App()

CloudcruftDns(
    app, 'CloudcruftDns',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftEgress(
    app, 'CloudcruftEgress',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftIpv4(
    app, 'CloudcruftIpv4',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftIpv6(
    app, 'CloudcruftIpv6',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftMx(
    app, 'CloudcruftMx',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftRdap(
    app, 'CloudcruftRdap',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftSpf(
    app, 'CloudcruftSpf',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CloudcruftStack(
    app, 'CloudcruftStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','Tacklebox')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/cloudcruft')

app.synth()