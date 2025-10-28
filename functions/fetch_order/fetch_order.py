import json
from logging import getLogger, INFO
from datetime import datetime
from uuid import uuid4

HTTP_STATUS_CODE_OK = 200

logger = getLogger()
logger.setLevel(INFO)

def handler(event, context):
    logger.info(f"Executing fetch_order with event: {json.dumps(event)}")
    # Create and return order as JSON with required fields
    order = {
        'id': str(uuid4()),
        'description': 'Sample order description',
        'created_date': datetime.now().isoformat(),
        'modified_date': datetime.now().isoformat()
    }
    return {
        'statusCode': HTTP_STATUS_CODE_OK,
        'body': order
    }
