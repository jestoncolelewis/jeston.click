from constructs import Construct
from aws_cdk import(
    Stack,
    Environment
)
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep,
    ManualApprovalStep
)
from .buckets import name
from .pipeline_stage import PipelineStage

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, "Pipeline",
            synth=ShellStep(
            "Synth",
            input=CodePipelineSource.git_hub("jestoncolelewis/{}".format(name), "main"),
            commands= [
                "npm install 0g aws-cdk",
                "python -m pip install -r requirements.txt",
                "cdk synth"
            ]
            )
        )

        test = PipelineStage(self, "Test")
        prod = PipelineStage(self, "Prod")

        pipeline.add_stage(test,
                           post= [
                               ShellStep("Validate Endpoint", 
                                         commands=["curl -Ssf https://{}".format(name)])
                           ])
        pipeline.add_stage(prod,
                           pre=[
                               ManualApprovalStep("PromoteToProd")
                           ])