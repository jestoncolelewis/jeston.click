#!/usr/bin/env python3
import os

import aws_cdk as cdk

from jestonclick.jestonclick_stack import JestonClickStack


app = cdk.App()
JestonClickStack(app, "JestonClickStack", env=cdk.Environment(account="706391136734", region="us-east-1"))

app.synth()
