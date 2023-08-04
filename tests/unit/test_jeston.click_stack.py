import aws_cdk as core
import aws_cdk.assertions as assertions

from jeston.click.jeston.click_stack import JestonClickStack

# example tests. To run these tests, uncomment this file along with the example
# resource in jeston.click/jeston.click_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = JestonClickStack(app, "jeston-click")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
