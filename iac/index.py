import boto3
import datetime
import json

name = "jestondotclick-page-views"
dynamodb = boto3.client("dynamodb")
dynamor = boto3.resource("dynamodb")
table = dynamor.Table(name)

now = datetime.datetime.now().timestamp()
now = "{}".format(now)

key = {"primary-key": {"N": "0"}}


def lambda_handler(event, context):
    if event.get("routeKey") == "GET /jestondotclick-page-views":
        response = dynamodb.get_item(
            TableName = name,
            Key = key
        )
        view = response["Item"]['view-num']['N']
        
        item = int(view)
        item += 1
        item = "{}".format(item)
        
        response = dynamodb.update_item(
            TableName = name,
            Key = key,
            ExpressionAttributeNames = {
                "#DT": "date-time",
                "#VN": "view-num"
            },
            ExpressionAttributeValues = {
                ":d": {"N": now},
                ":v": {"N": item}
            },
            UpdateExpression = "SET #DT = :d, #VN = :v",
        )
        return view
