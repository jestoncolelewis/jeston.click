#!/usr/bin/env python3
import os

import aws_cdk as cdk

from jestonclick.jestonclick_stack import JestonClickStack
from jestonclick.pipeline_stack import PipelineStack

env = cdk.Environment(account="706391136734", region="us-east-1")
app = cdk.App()
# JestonClickStack(app, "JestonClickStack", env=env)
PipelineStack(app, "JestonClickWebsite", env=env)

app.synth()
