import json
import boto3

# Connect to DynamoDB outside the handler (faster on repeat calls)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST'
}

def reply(status, message):
    return {
        'statusCode': status,
        'headers': HEADERS,
        'body': json.dumps({'message': message})
    }

def lambda_handler(event, context):
    # 1. Read the username and password sent by the web page
    try:
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            body = event
        input_username = body.get('username', '').strip()
        input_password = body.get('password', '').strip()
    except Exception:
        return reply(400, 'Invalid input data format.')

    # 2. Check the fields are not empty
    if not input_username or not input_password:
        return reply(400, 'Please enter both username and password.')

    # 3. Look up the user in DynamoDB
    try:
        response = table.get_item(Key={'username': input_username})

        if 'Item' in response:
            db_password = response['Item'].get('password')
            if input_password == db_password:
                return reply(200, f'Login Successful! Welcome, {input_username}.')

        # User not found OR wrong password
        return reply(401, 'Invalid Credentials. Try again.')

    except Exception as e:
        return reply(500, f'Database Connection Error: {str(e)}')