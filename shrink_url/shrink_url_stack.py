from aws_cdk import (
    Duration,
    Stack,
    aws_lambda,
    aws_dynamodb,
)
from constructs import Construct
import sys
sys.path.append("..")
from url_shortener_constructs.lambda_construct import LambdaConstruct,lambdaProps
from url_shortener_constructs.dynamodb_table import DynamoDBConstruct, dynamodDBProps
from url_shortener_constructs.apigw import ApiGWConstruct, apiGWProps


class ShrinkUrlStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "ShrinkUrlQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # LAMBDAS

        get_lambda_props = lambdaProps(
            function_name = "getshorturl",
            description="get short url lambda",
            runtime = aws_lambda.Runtime.PYTHON_3_9,
            timeout = Duration.seconds(120),
            code= aws_lambda.Code.from_asset("lambda_code/getshorturl/lambda_function.py.zip"),
            handler= "lambda_function.lambda_handler",
            environment= {
                "DYNAMODB_TABLE" : "url-shortener",
            }
        )

        getshorturl_lambda = LambdaConstruct(self, id="getshorturl", props=get_lambda_props) 

        admin_lambda_props = lambdaProps(
            function_name = "admin",
            description="admin lambda",
            runtime = aws_lambda.Runtime.PYTHON_3_9,
            timeout = Duration.seconds(120),
            code= aws_lambda.Code.from_asset("lambda_code/admin/lambda_function.py.zip"),
            handler= "lambda_function.lambda_handler",
            environment= {
                "DYNAMODB_TABLE" : "url-shortener",
            }
        )

        admin_lambda = LambdaConstruct(self, id="admin", props=admin_lambda_props)

        # DYNAMODB

        dynamodb_props = dynamodDBProps(
            table_name="url-shortener",
            partition_key = aws_dynamodb.Attribute(
                name="url",
                type=aws_dynamodb.AttributeType.STRING,
            ),
        )
        
        shortener_db = DynamoDBConstruct(self, id="shortener-db", props=dynamodb_props)
        shortener_table = shortener_db.table

        # Lambda DB access
        shortener_table.grant_read_write_data(admin_lambda.function)
        shortener_table.grant_read_write_data(getshorturl_lambda.function)

        # APIGW
        apigw_props = apiGWProps(
            swagger="swagger.yaml",
            geturl_lambda=getshorturl_lambda.function,
            admin_lambda=admin_lambda.function
        )

        ApiGWConstruct(self, id="shortener-apigw", props=apigw_props)





