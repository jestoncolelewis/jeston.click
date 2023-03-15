from functions import *
import os

name = 'jestondotclick-page-views'

# s3 variables
path = os.getcwd()

file = 'index.zip'

path = path + '/' + file

# dynamo variables
keys = [
    {
        'AttributeName': 'date-time',
        'KeyType': 'HASH'
    }
]

attributes = [
    {
        'AttributeName': 'date-time',
        'AttributeType': 'N'
    }
]

key = build_bucket(name, path, file)

# lambda variables
lang = 'python3.9'

iam = 'arn:aws:iam::706391136734:role/service-role/microRole'

code = [name, key]

description = 'function for retrieving and updating page views'


build_dynamo(name, keys, attributes)
build_lambda(name, lang, iam, code, description)