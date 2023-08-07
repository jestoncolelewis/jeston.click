from constructs import Construct
from aws_cdk import(
    Stack,
    Environment
)
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep
)
from .buckets import name

class ProdPipeline(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(
            self, "Pipeline",
            pipeline_name="FrontEndPipeline",
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