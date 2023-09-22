"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import pulumi_synced_folder as synced_folder

path = "./www"
index_document = "index.html"
error_document = "404error.html"
website_name = "jeston.click"
www_name = "www.{}".format(website_name)

zone = aws.route53.Zone("zone",
    comment="",
    name=website_name,
    opts=pulumi.ResourceOptions(protect=True))

main_bucket = aws.s3.Bucket(
    website_name,
    bucket=website_name,
    website=aws.s3.BucketWebsiteArgs(
        index_document=index_document,
        error_document=error_document
    )
)
ownership_controls = aws.s3.BucketOwnershipControls(
    "ownership-controls",
    bucket=main_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="ObjectWriter"
    )
)
public_access_block = aws.s3.BucketPublicAccessBlock(
    "public_access_block",
    bucket=main_bucket.id,
    block_public_acls=False
)
bucket_folder = synced_folder.S3BucketFolder(
    "bucket-folder",
    acl="public-read",
    bucket_name=main_bucket.bucket,
    path=path,
    opts=pulumi.ResourceOptions(depends_on=[
        ownership_controls,
        public_access_block
    ])
)
www_bucket = aws.s3.Bucket(
    www_name,
    bucket=www_name,
    website=aws.s3.BucketWebsiteArgs(
        redirect_all_requests_to=website_name
    )
)