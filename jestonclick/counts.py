from constructs import Construct
from aws_cdk import (
    aws_lambda as lamb,
    aws_apigateway as api,
    aws_iam as iam
)

class Counts(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        form = lamb.Function(
            self, "Counter",
            runtime=lamb.Runtime.PYTHON_3_9,
            code=lamb.Code.from_asset("lambda"),
            handler="page_count.handler"
        )
        form.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:ListStreams",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            resources=["*"] 
        ))

        options = lamb.Function(
            self, "Options",
            runtime=lamb.Runtime.PYTHON_3_9,
            code=lamb.Code.from_asset("lambda"),
            handler="options_return.handler"
        )


        gateway = api.LambdaRestApi(
            self, "CountLambdaGateway",
            handler=form,
            proxy=True
        )
        gateway.root.add_method("GET")
        gateway.root.add_method("POST")
        gateway.root.add_method("HEAD")
        gateway.root.add_method("OPTIONS", api.LambdaIntegration(options))