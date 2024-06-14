#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudcruft.cloudcruft_egress import CloudcruftEgress
from cloudcruft.cloudcruft_match import CloudcruftMatch
from cloudcruft.cloudcruft_stack import CloudcruftStack

app = cdk.App()

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

CloudcruftMatch(
    app, 'CloudcruftMatch',
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