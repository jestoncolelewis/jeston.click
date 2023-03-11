import boto3

# resources to setup
dynamodb = boto3.client('dynamodb')

table = dynamodb.create_table(
    TableName = 'page_views',
    KeySchema = [
        {
            'AttributeName': 'view_num',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'date_time',
            'KeyType': 'RANGE'
        },
    ],
    AttributeDefinitions = [
        {
            'AttributeName': 'view_num',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'date_time',
            'AttributeType': 'N'
        },
    ],
    ProvisionedThroughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)