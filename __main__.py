"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

zone = aws.route53.Zone("zone",
    comment="",
    name="jeston.click",
    opts=pulumi.ResourceOptions(protect=True))