import boto3

# resources to setup
dynamodb = boto3.resource('dynamodb')
lambda_function = boto3.client('lamba')