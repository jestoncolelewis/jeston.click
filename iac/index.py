import boto3
import json

dynamodb = boto3.client("dynamodb")
table = dynamodb.Table("page_views")

Key = {"view_num": "", "date_time": ""}


def lambda_handler(event, context):
    if event.get("routeKey") == "GET /items":
        response = table.get_item(Key)
        item = response["Item"]
        return item
    if event.get("routeKey") == "PUT /items":
        response = table.update_item(
            Key,
            UpdateExpression="SET view_num = :vall",
            ExpressionAttributeValues={":vall": item},
        )
