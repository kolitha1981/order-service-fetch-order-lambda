import json
from logging import getLogger, INFO
from os import environ

import boto3

dynamo_db_table = None
HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_NOT_FOUND = 404
HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR = 500

logger = getLogger()
logger.setLevel(INFO)

def handler(event, context):
    logger.info(f"Executing fetch_order with event: {json.dumps(event)}")
    try:
        if 'pathParameters' in event and event['pathParameters']:
            order_id = event['pathParameters'].get('order_id')
            if not order_id:
                return {
                    'statusCode': 400,
                    'body': f"Missing path parameter: order_id"
                }

        # Fetch the order from DynamoDB
        global dynamo_db_table
        if dynamo_db_table is None:
            dynamod_db_client = boto3.resource('dynamodb')
            dynamo_db_table_name = environ.get('DYNAMODB_TABLE_NAME', 'Orders')
            dynamo_db_table = dynamod_db_client.Table(dynamo_db_table_name)
        response = dynamo_db_table.get_item(
            Key={'order_id': order_id}
        )
        # Check if the order exists
        if 'Item' not in response:
            return {
                'statusCode': HTTP_STATUS_CODE_NOT_FOUND,
                'body': F"Order with order_id {order_id} not found"
            }
        return {
            'statusCode': HTTP_STATUS_CODE_OK,
            'body': response['Item']
        }
    except Exception as e:
        logger.error(f"Fetching the order for order id {order_id} failed due to {str(e)}")
        return {
            'statusCode': HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR,
            'body': f"Fetching the order for order id {order_id} failed due to {str(e)}"
        }