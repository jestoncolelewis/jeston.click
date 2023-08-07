from constructs import Construct
from aws_cdk import(
    Stage
)
from .jestonclick_stack import JestonClickStack

class PipelineStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        website = JestonClickStack(self, "WebSite")
