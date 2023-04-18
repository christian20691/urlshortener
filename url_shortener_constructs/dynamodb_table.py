from aws_cdk import aws_dynamodb
import aws_cdk
from constructs import Construct

# partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),

class dynamodDBProps(dict):
    table_name: str
    partition_key: aws_dynamodb.Attribute


class DynamoDBConstruct(Construct):
    def __init__(self, scope: "Construct", id: str, props : dynamodDBProps) -> None:
        super().__init__(scope, id)

        self.table = aws_dynamodb.Table(self, id, **props)