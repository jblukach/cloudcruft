import cdk_nag

from aws_cdk import (
    Aspects,
    Stack,
    aws_lambda as _lambda,
    aws_sns as _sns
)

from constructs import Construct

class CloudcruftStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYER ###

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
        )

    ### TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':monitor'
        )

    ### CDK NAG ###

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks()
        )

        Aspects.of(self).add(
            cdk_nag.HIPAASecurityChecks()    
        )

        Aspects.of(self).add(
            cdk_nag.NIST80053R5Checks()
        )

        Aspects.of(self).add(
            cdk_nag.PCIDSS321Checks()
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [

            ]
        )
