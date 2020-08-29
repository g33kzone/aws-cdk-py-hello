import os
from aws_cdk import (
    core as core,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3_notify,
    aws_s3_deployment as s3deploy
)


class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # self.node.apply_aspect(core.Aws.ACCOUNT_ID)

        dap_environment = os.environ["ENV_VALUE"]

        src_bucket_name = self.node.try_get_context("src_bucket_name")
        src_bucket_name = src_bucket_name.replace("env", dap_environment)

        dest_bucket_name = self.node.try_get_context("dest_bucket_name")
        dest_bucket_name = dest_bucket_name.replace("env", dap_environment)

        source_bucket = s3.Bucket(
            self, 'sourceBucket',
            bucket_name=src_bucket_name,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        destination_bucket = s3.Bucket(
            self, 'destinationBucket',
            bucket_name=dest_bucket_name,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        lambda_iam_role = iam.Role(
            self, 'lambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            role_name="lambda-hello-role",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchFullAccess"
            )]
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
                'destination_bucket': dest_bucket_name
            }
        )

        notification = s3_notify.LambdaDestination(my_lambda)

        source_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT, notification)

        s3deploy.BucketDeployment(
            self, 'DeployGlueJob',
            sources=[s3deploy.Source.asset("glue")],
            destination_bucket=destination_bucket,
            destination_key_prefix="web/dap"
        )
