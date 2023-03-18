import boto3
import datetime
import json

name = "jestondotclick-page-views"
dynamodb = boto3.client("dynamodb")
dynamor = boto3.resource("dynamodb")
table = dynamor.Table(name)

now = datetime.datetime.now().timestamp()
now = "{}".format(now)

# how do I get the latest item?
key = {"date-time": {"N": "1679179226.926753"}}


def lambda_handler(event, context):
    if event.get("routeKey") == "GET /items":
        response = dynamodb.get_item(
            TableName = name,
            Key = key
        )
        view = response["Item"]['view-num']['N']
        
        item = int(view)
        item += 1
        item = "{}".format(item)
        
        response = dynamodb.put_item(
            TableName = name,
            Item = {
                "date-time": {
                    "N": now
                },
                "view-num": {
                    "N": item
                }
            },
        )
        return view
