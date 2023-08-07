from constructs import Construct
from aws_cdk import(
    Stage
)
from .pipeline_stack import PipelineStack

class PipelineStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service = PipelineStack(self, "WebSite")
