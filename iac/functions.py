import boto3
import botocore.exceptions

# resources to setup
s3 = boto3.client('s3')
s3r = boto3.resource('s3')
dynamodb = boto3.client('dynamodb')
lamb = boto3.client('lambda')
api = boto3.client('apigatewayv2')

# create bucket
def build_bucket(name, path, file):
    try:
        s3.create_bucket(
            Bucket = name,
            CreateBucketConfiguration = {
                'LocationConstraint': 'us-west-2'
            }
        )
        s3r.meta.client.upload_file(path, name, file)
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
    response = s3.list_objects(Bucket = name)
    objects = list(response.items())
    file = objects[3][1][0].get('Key')
    return file

# build table
def build_dynamo(name, keys, attdef):
    try:
        dynamodb.create_table(
            TableName = name,
            KeySchema = keys,
            AttributeDefinitions = attdef,
            ProvisionedThroughput = {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))

# build function
def build_lambda(name, lang, role, code, desc):
    try:
        response = lamb.create_function(
            Runtime = lang,
            Role = role,
            Code = {
                'S3Bucket': code[0],
                'S3Key': code[1]
            },
            Description = desc,
            FunctionName = name,
            Handler = 'index.lambda_handler'
        )
        return response.get('FunctionArn')
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
        response = lamb.get_function(FunctionName = name)
        return response['Configuration']['FunctionArn']

# build api
def build_api(name, target):
    try:
        api.create_api(
            Name = name,
            ProtocolType = 'HTTP',
            CorsConfiguration = {
                'AllowOrigins': ['*']
            },
            Target = target
        )
    except botocore.exceptions.ClientError as err:
        print('{}'.format(err.response['Error']['Message']))
    