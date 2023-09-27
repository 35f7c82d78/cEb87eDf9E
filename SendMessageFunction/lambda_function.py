import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebSocketMessages')

def lambda_handler(event, context):
    # Extract the connection ID and action from WebSocket event
    connection_id = event.get('requestContext', {}).get('connectionId')
    body = json.loads(event.get('body', '{}'))
    action = body.get('action', '')
    message = body.get('message', '')
    
    print(f'WebSocket URL: wss://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}')
    
    if action == 'sendMessage':
        response = table.put_item(
            Item={
                'SenderID': connection_id,
                'MessageID': 'msg1',  # Replace with a proper message ID
                'Message': message
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent!')
        }

    return {
        'statusCode': 400,
        'body': json.dumps('Invalid action!')
    }
