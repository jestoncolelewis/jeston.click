import boto3
import json

ses = boto3.client("sesv2")

def handler(event, context):
    body = event["body"]
    print(body)
    body = json.loads("{}".format(body))
    replyto = body["email"]
    subject = body["subject"]
    message = "Name: " + body["name"] + "\n" + "Message: " + body["message"]
    response = ses.send_email(
        FromEmailAddress = "web@jestonlewiscreative.com",
        Destination = {"ToAddresses": ["info@jestonlewiscreative.com"]},
        ReplyToAddresses = [replyto],
        Content = {
            "Simple": {
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": message}}
            }
        }
    )
    return response
    