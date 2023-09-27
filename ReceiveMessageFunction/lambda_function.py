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
    message_id = body.get('messageId', '')
    
    print(f'WebSocket URL: wss://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}')
    
    if action == 'receiveMessage':
        response = table.get_item(
            Key={
                'SenderID': connection_id,
                'MessageID': message_id
            }
        )
        
        message = response.get('Item', {}).get('Message', 'No message found!')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
        
    return {
        'statusCode': 400,
        'body': json.dumps('Invalid action!')
    }
