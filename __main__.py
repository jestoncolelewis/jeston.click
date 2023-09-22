"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

path = "./www"
website_name = "jeston.click"

zone = aws.route53.Zone("zone",
    comment="",
    name=website_name,
    opts=pulumi.ResourceOptions(protect=True))

main_bucket = aws.s3.Bucket(
    website_name,
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
        error_document="404error.html"
    )
)

www_bucket = aws.s3.Bucket(
    "www.{}".format(website_name),
    website=aws.s3.BucketWebsiteArgs(
        redirect_all_requests_to=website_name
    )
)