from datetime import datetime, timezone
from logging import getLogger, INFO
from os import environ
from uuid import uuid4
import boto3

dynamo_db_table = None

HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR = 500

logger = getLogger()
logger.setLevel(INFO)
class SaveOrderFailedException(Exception):
    pass

def lambda_handler(event, context):
    logger.info(f"Executing save_order with event: {event}")
    global dynamo_db_table
    if dynamo_db_table is None:
        dynamodb_client = boto3.resource('dynamodb')
        dynamo_db_table_name = environ.get('ORDERS_TABLE_NAME', 'Orders')
        dynamo_db_table = dynamodb_client.Table(dynamo_db_table_name)
    try:
        order_id = event.get('order_id', str(uuid4())).strip()
        order_description = event.get('order_description', 'Test order description').strip()
        created_date = datetime.now(timezone.utc).isoformat()
        last_updated_date = datetime.now(timezone.utc).isoformat()
        order_item = {
            'order_id': order_id,
            'order_description': order_description,
            'created_date': created_date,
            'last_updated_date': last_updated_date
        }
        response = dynamo_db_table.put_item(Item=order_item)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            error_message = f"Failed to save order into dynamo db table: {response}"
            logger.error(error_message)
            return {
                'statusCode': HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR,
                'body': error_message
            }
        return {
            'statusCode': HTTP_STATUS_CODE_OK,
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
            'statusCode': HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR,
            'body': error_message
        }


