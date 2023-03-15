import boto3
import datetime
import json

dynamodb = boto3.client("dynamodb")
table = dynamodb.Table("page_views")

now = datetime.datetime.now()
now = f'{now}'

# how do I get the latest item?
Key = {"date-time": now}


def lambda_handler(event, context):
    if event.get("routeKey") == "GET /items":
        response = table.get_item(Key)
        item = response["Item"]
        return item
    if event.get("routeKey") == "PUT /items":
        response = table.update_item(
            Key,
            UpdateExpression="SET view_num = :vall",
            # need to figure out what value to add
            ExpressionAttributeValues={":vall": ''},
        )
        return response
