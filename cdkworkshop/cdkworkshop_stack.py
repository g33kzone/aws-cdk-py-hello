from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,

)


class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_lambda = _lambda.Function(
            self,'HelloHandler',
            function_name='hellohandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler'
        )

        apigw.LambdaRestApi(
            self,'Endpoint',
            handler=my_lambda,
        )



