import aws_cdk
from aws_cdk import aws_lambda
from constructs import Construct

class lambdaProps(dict):
    function_name: str
    description: str
    runtime: aws_lambda.Runtime
    timeout: aws_cdk.Duration
    code: aws_lambda.Code
    handler: str
    environment: dict

class LambdaConstruct(Construct):
    def __init__(self, scope: "Construct", id: str, props: lambdaProps) -> None:
        super().__init__(scope, id)
        
        self.function = aws_lambda.Function(self, id, **props)
