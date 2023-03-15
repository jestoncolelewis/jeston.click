from functions import *
import os

name = 'jeston.click-page-views'

# s3 variables
path = os.getcwd()

file = 'index.zip'

path = path + '/' + file

# dynamo variables
keys = [
    {
        'AttributeName': 'view-num',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'date-time',
        'KeyType': 'RANGE'
    },
]

attributes = [
    {
        'AttributeName': 'view-num',
        'AttributeType': 'N'
    },
    {
        'AttributeName': 'date-time',
        'AttributeType': 'N'
    },
]

key = build_bucket(name, path, file)

# lambda variables
lang = 'python3.9'

iam = 'arn:aws:iam::706391136734:role/service-role/microRole'

code = [name, key]


build_dynamo(name, keys, attributes)
build_lambda(name, lang, iam, code)