import json
import boto3
from os import environ
from datetime import datetime, timezone
from uuid import uuid4
from logging import getLogger, INFO

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = None
table = dynamodb.Table(table_name)
logger = getLogger()
logger.setLevel(INFO)

class SaveOrderFailedException(Exception):
    pass

def lambda_handler(event, context):
    global table_name
    if table_name is None:
        table_name = environ.get('ORDERS_TABLE_NAME', 'Orders')
    try:
        order_id = event.get('order_id', str(uuid4())).strip()
        order_description = event.get('order_description', 'Test order description').strip()
        created_date = datetime.now(timezone.utc).isoformat()
        last_updated_date = datetime.now(timezone.utc).isoformat()
        # Prepare the item to save
        order_item = {
            'order_id': order_id,
            'order_description': order_description,
            'created_date': created_date,
            'last_updated_date': last_updated_date
        }
        response = table.put_item(Item=order_item)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            error_message = f"Failed to save order into dynamo db table: {response}"
            logger.error(error_message)
            raise SaveOrderFailedException(error_message)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': order_item
        }
    except Exception as e:
        error_message = f"Exception occurred while saving order into dynamo db table: {str(e)}"
        logger.error(error_message)
        return {
            'statusCode': 500,
            'body': error_message
        }


