import json
import boto3
import os

table = os.environ['DYNAMODB_TABLE']

def get_dynamodb_client():
    return boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        response = {"message": "The url entries has been created", "error": ""}
        
        dynamodb = get_dynamodb_client()    
        dynamodb.put_item(
            TableName=table,
            Item={
                'url': {'S': data.get('url')},
                'shorturl': { 'S': data.get('shorturl')},
                })        
        
        return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    'code': 200,
                    'name': 'OK',
                    'message': 'Success',
                    'body': response['message'],
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
                    "message":'An error occurred while creating url: ' + str(e),
                    "body": []
                })
            }        
