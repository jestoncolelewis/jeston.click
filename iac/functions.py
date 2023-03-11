import boto3

# resources to setup
dynamodb = boto3.client('dynamodb')
lamb = boto3.client('lambda')

# build table
def build_dynamo(name, keys, attdef):
    dynamodb.create_table(
        TableName = name,
        KeySchema = keys,
        AttributeDefinitions = attdef,
        ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

# build function
def build_lambda(name, lang, role, code):
    lamb.create_function(
        FunctionName = name,
        Runtime = lang,
        Role = role,
        Code = {
            'ZipFile': code[0],
            'S3Bucket': code[1],
            'S3Key': code[2],
            'S3ObjectVersion': code[3],
            'ImageUri': code[4]
        }
    )