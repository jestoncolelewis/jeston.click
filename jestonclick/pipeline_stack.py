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
                "npm install -g aws-cdk",
                "python -m pip install -r requirements.txt",
                "cdk synth"
            ]
            )
        )
        prod = PipelineStage(self, "Prod")
        pipeline.add_stage(prod)