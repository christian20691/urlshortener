import aws_cdk
from aws_cdk import aws_lambda
from constructs import Construct

# id=experience_api_lambda_name,
# function_name=experience_api_lambda_name,
# description="Experiences API Lambda",
# runtime=aws_lambda.Runtime.PYTHON_3_9,
# timeout=lambda_timeout_seconds,
# code=aws_lambda.Code.from_asset(f"{stack_path}/bazel-bin/app/src/data_service/experience_api/lambda_archive.zip"),
# handler="lambda_function.lambda_handler",
# environment=typing.cast(typing.Dict[str, str], lambda_environment),
# allow_public_subnet=False,

## Code
#lambda_code = aws_lambda.Code.from_asset(os.path.join("/lambda_code/", "lambda_handler.py"))


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