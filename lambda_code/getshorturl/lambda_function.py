import simplejson as json
import boto3
import os
from boto3.dynamodb.conditions import Key


table = os.environ['DYNAMODB_TABLE']

def get_dynamodb_client():
   return boto3.client('dynamodb')

def lambda_handler(event, context):    
    try:
        data = json.loads(event['body'])
        url = data.get('url')
        dynamodb = boto3.client('dynamodb')
        
        query_response = dynamodb.get_item(
                Key={
                    'url': {"S": "https://longurl.com/asd"},
                },
                TableName=table
            )
        
        return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    'code': 200,
                    'name': 'OK',
                    'message': 'Success',
                    'body': query_response,
                })
            }

    except Exception as e:
        return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "code": 500,
                    "name": 'SYSTEM.INTERNAL_ERROR',
                    "message":'An error occurred while querying url: ' + str(e),
                    "body": []
                })
            }