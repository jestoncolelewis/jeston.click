from functions import *
import os

name = 'page_views'

# s3 variables
path = os.getcwd()

file = 'index.zip'

# dynamo variables
keys = [
    {
        'AttributeName': 'view_num',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'date_time',
        'KeyType': 'RANGE'
    },
]

attributes = [
    {
        'AttributeName': 'view_num',
        'AttributeType': 'N'
    },
    {
        'AttributeName': 'date_time',
        'AttributeType': 'N'
    },
]

key = build_bucket(name, path, file)

# lambda variables
lang = 'python3.9'

iam = ''

code = [name, key]


build_dynamo(name, keys, attributes)
build_lambda(name, lang, iam, code)