import boto3

# resources to setup
s3 = boto3.client('s3')
s3r = boto3.resource('s3')
dynamodb = boto3.client('dynamodb')
lamb = boto3.client('lambda')

# create bucket
def build_bucket(name, path, file):
    s3.create_bucket(
        Bucket = name,
        CreateBucketConfiguration = {
            'LocationConstraint': 'us-west-2'
        }
    )
    s3r.meta.client.upload_file(path, name, file)
    response = s3.list_objects(Bucket = name)
    objects = list(response.items())
    file = objects[3][1][0].get('Key')
    return file

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
            'S3Bucket': code[0],
            'S3Key': code[1]
        }
    )