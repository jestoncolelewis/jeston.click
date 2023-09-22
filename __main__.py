"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import pulumi_synced_folder as synced_folder

path = "./www"
index_document = "index.html"
error_document = "404error.html"
website_name = "jeston.click"
www_name = "www.{}".format(website_name)

# Imported zone
zone = aws.route53.Zone("zone",
    comment="",
    name=website_name,
    opts=pulumi.ResourceOptions(protect=True))

# Bucket creation and management
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

# CDN Creation
cdn = aws.cloudfront.Distribution(
    "cdn",
    enabled=True,
    origins=[
        aws.cloudfront.DistributionOriginArgs(
            origin_id=main_bucket.arn,
            domain_name=main_bucket.website_endpoint,
            custom_origin_config=aws.cloudfront.DistributionOriginCustomOriginConfigArgs(
                origin_protocol_policy="http-only",
                http_port=80,
                https_port=443,
                origin_ssl_protocols=["TLSv1.2"],
            ),
        )
    ],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        target_origin_id=main_bucket.arn,
        viewer_protocol_policy="redirect-to-https",
        allowed_methods=[
            "GET",
            "HEAD",
            "OPTIONS",
        ],
        cached_methods=[
            "GET",
            "HEAD",
            "OPTIONS",
        ],
        default_ttl=600,
        max_ttl=600,
        min_ttl=600,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=True,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="all",
            ),
        ),
    ),
    price_class="PriceClass_100",
    custom_error_responses=[
        aws.cloudfront.DistributionCustomErrorResponseArgs(
            error_code=404,
            response_code=404,
            response_page_path=f"/{error_document}",
        )
    ],
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ),
)

# Certificate Creation
certificate = aws.acm.Certificate(
    "certificate",
    domain_name=website_name,
    validation_method="DNS"
)
cert_validation = aws.route53.Record(
    "cert-validation",
    name=certificate.domain_validation_options[0].resource_record_name,
    records=[certificate.domain_validation_options[0].resource_record_value],
    ttl=60,
    type=certificate.domain_validation_options[0].resource_record_type,
    zone_id=zone.id
)

# Outputs
pulumi.export("cdnURL", pulumi.Output.concat("https://", cdn.domain_name))
with open("./README.md") as f:
    pulumi.export("readme", f.read())