from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_certificatemanager as _acm,
    aws_cloudfront as _cloudfront,
    aws_cloudfront_origins as _origins,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_route53 as _route53,
    aws_route53_targets as _r53targets,
    aws_ssm as _ssm
)

from constructs import Construct

class CloudcruftSpf(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYER ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        dnspython = _lambda.LayerVersion.from_layer_version_arn(
            self, 'dnspython',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:dnspython:6'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:14'
        )

        netaddr = _lambda.LayerVersion.from_layer_version_arn(
            self, 'netaddr',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:netaddr:8'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

    ### LAMBDA ###

        compute = _lambda.Function(
            self, 'compute',
            function_name = 'spf',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('api/spf'),
            timeout = Duration.seconds(13),
            handler = 'spf.handler',
            environment = dict(
                AWS_ACCOUNT = account
            ),
            memory_size = 1024,
            retry_attempts = 0,
            role = role,
            layers = [
                dnspython,
                getpublicip,
                netaddr
            ]
        )

        url = compute.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+compute.function_name,
            retention = _logs.RetentionDays.THIRTEEN_MONTHS,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### HOSTZONE ###

        hostzoneid = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'hostzoneid',
            parameter_name = '/r53/tundralabs.net'
        )

        hostzone = _route53.HostedZone.from_hosted_zone_attributes(
             self, 'hostzone',
             hosted_zone_id = hostzoneid.string_value,
             zone_name = 'tundralabs.net'
        )   

        cdnlogs = _logs.LogGroup(
            self, 'cdnlogs',
            log_group_name = '/aws/cloudfront/spftundralabsnet',
            retention = _logs.RetentionDays.THIRTEEN_MONTHS,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### ACM CERTIFICATE ###

        acm = _acm.Certificate(
            self, 'acm',
            domain_name = 'spf.tundralabs.net',
            validation = _acm.CertificateValidation.from_dns(hostzone)
        )

    ### CLOUDFRONT ###

        distribution = _cloudfront.Distribution(
            self, 'distribution',
            comment = 'spf.tundralabs.net',
            default_behavior = _cloudfront.BehaviorOptions(
                origin = _origins.FunctionUrlOrigin(url),
                viewer_protocol_policy = _cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy = _cloudfront.CachePolicy.CACHING_DISABLED
            ),
            domain_names = [
                'spf.tundralabs.net'
            ],
            error_responses = [
                _cloudfront.ErrorResponse(
                    http_status = 404,
                    response_http_status = 200,
                    response_page_path = '/'
                )
            ],
            certificate = acm,
            minimum_protocol_version = _cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            price_class = _cloudfront.PriceClass.PRICE_CLASS_100,
            http_version = _cloudfront.HttpVersion.HTTP2_AND_3,
            enable_ipv6 = True
        )

    ### DNS ENTRY ###

        cdnurl = _route53.ARecord(
            self, 'cdnurl',
            zone = hostzone,
            record_name = 'spf.tundralabs.net',
            target = _route53.RecordTarget.from_alias(_r53targets.CloudFrontTarget(distribution))
        )
