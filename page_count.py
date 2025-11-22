import boto3
import datetime

name = "jestondotclick-page-views"
dynamodb = boto3.client("dynamodb")
key = {"pk": {"N": "0"}}


def handler(event, context):
    # Calculate timestamp at request time, not import time
    now = str(int(datetime.datetime.now().timestamp()))

    response = dynamodb.get_item(
        TableName=name,
        Key=key
    )
    view = response["Item"]["view-num"]["N"]

    item = str(int(view) + 1)

    dynamodb.update_item(
        TableName=name,
        Key=key,
        ExpressionAttributeNames={
            "#DT": "date-time",
            "#VN": "view-num"
        },
        ExpressionAttributeValues={
            ":d": {"N": now},
            ":v": {"N": item}
        },
        UpdateExpression="SET #DT = :d, #VN = :v",
    )
    return view