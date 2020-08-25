from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3_notify,
)


class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # self.node.apply_aspect(core.Aws.ACCOUNT_ID)

        source_bucket = s3.Bucket(
            self, 'sourceBucket',
            bucket_name='source-g33kzone',
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        destination_bucket = s3.Bucket(
            self, 'destinationBucket',
            bucket_name='destination-g33kzone',
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        lambda_iam_role = iam.Role(
            self, 'lambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            role_name="lambda-hello-role"
        )

        lambda_layer = _lambda.LayerVersion(
            self, 'lambdaLayer',
            code=_lambda.Code.asset('lambda_layers/python_libs.zip'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_7],
            layer_version_name='lambda-layer-cdk',
            description='A Lambda layer for common utility'
        )

        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            role=lambda_iam_role,
            function_name='hellohandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler',
            layers=[lambda_layer],
            memory_size=128,
            environment={
                'env_test_key': 'AWS CDK',
            }
        )

        # notification = s3_notify.LambdaDestination(my_lambda)

        # source_bucket.add_event_notification(
        #     s3.EventType.OBJECT_CREATED, notification)

        # apigw.LambdaRestApi(
        #     self, 'Endpoint',
        #     handler=my_lambda,
        # )
