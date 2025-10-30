import json
from logging import getLogger, INFO
from datetime import datetime
from uuid import uuid4
import random

HTTP_STATUS_CODE_OK = 200

logger = getLogger()
logger.setLevel(INFO)

def handler(event, context):
    logger.info(f"Executing fetch_order with event: {json.dumps(event)}")
    #Generate random number between 1 and 4 and throw exception if odd
    random_number = random.randint(1, 5)
    logger.info(f"Generated random number: {random_number}")
    if random_number % 2 == 0:
        raise Exception(f"Random number {random_number} is odd, throwing exception")

    # Create and return order as JSON with required fields
    order = {
        'id': str(uuid4()),
        'description': 'Sample order description',
        'created_date': datetime.now().isoformat(),
        'modified_date': datetime.now().isoformat()
    }
    return {
        'statusCode': HTTP_STATUS_CODE_OK,
        'body': json.dumps(order)
    }
