import boto3
import datetime

name = "jestondotclick-page-views"
dynamodb = boto3.client("dynamodb")
dynamor = boto3.resource("dynamodb")
table = dynamor.Table(name)

now = datetime.datetime.now().timestamp()
now = "{}".format(now)

key = {"pk": {"N": "0"}}


def handler(event, context):
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