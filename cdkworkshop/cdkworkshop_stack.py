from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam

)


class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # self.node.apply_aspect(core.Aws.ACCOUNT_ID)

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
            environment={
                'env_test_key': 'AWS CDK',
            }
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )
