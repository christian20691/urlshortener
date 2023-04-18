from aws_cdk import aws_iam, aws_apigateway, aws_lambda
import aws_cdk
import os
import yaml
from dataclasses import dataclass
from constructs import Construct

@dataclass
class apiGWProps(dict):
    swagger: str
    geturl_lambda : aws_lambda.Function
    admin_lambda: aws_lambda.Function

class ApiGWConstruct(Construct):
    def __init__(self, scope: "Construct", id: str, props : apiGWProps) -> None:
        super().__init__(scope, id)
        
        stack = aws_cdk.Stack.of(self)
        region = stack.region

        stack = aws_cdk.Stack.of(self)
        swagger = self.load_swagger(props.swagger)
        geturl_lambda = props.geturl_lambda
        admin_lambda = props.admin_lambda
        
        # Swagger update - lambda uri 
        swagger["paths"]["/getshorturl"]["post"]["x-amazon-apigateway-integration"]["uri"] = f"arn:aws:apigateway:{region}" f":lambda:path/2015-03-31/functions/" f"{geturl_lambda.function_arn}/invocations"
        swagger["paths"]["/admin"]["post"]["x-amazon-apigateway-integration"]["uri"] = f"arn:aws:apigateway:{region}" f":lambda:path/2015-03-31/functions/" f"{admin_lambda.function_arn}/invocations"

        rest_api_role = aws_iam.Role(self, id="rest-api-role", assumed_by=aws_iam.ServicePrincipal("apigateway.amazonaws.com"))

        rest_api_role.add_to_policy(
            aws_iam.PolicyStatement(
                actions=["lambda:InvokeFunction", "lambda:GetFunctionConfiguration"],
                effect=aws_iam.Effect.ALLOW,
                resources=[
                    geturl_lambda.function_arn,
                    admin_lambda.function_arn,
                ],
            )
        )

        # Swagger update - lambda role
        swagger["paths"]["/getshorturl"]["post"]["x-amazon-apigateway-integration"]["credentials"] = f"{rest_api_role.role_arn}"
        swagger["paths"]["/admin"]["post"]["x-amazon-apigateway-integration"]["credentials"] = f"{rest_api_role.role_arn}"

        self.rest_api = aws_apigateway.SpecRestApi(
            self,
            "url-shortener-rest-api",
            api_definition=aws_apigateway.ApiDefinition.from_inline(swagger),
        )

    @staticmethod
    def load_swagger(swagger_file: str) -> dict:
        with open(os.path.join("swaggers", swagger_file), "r", encoding="UTF-8") as file:
            return yaml.safe_load(file)