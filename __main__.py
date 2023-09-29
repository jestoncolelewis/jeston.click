import pulumi
import pulumi_archive as archive
import pulumi_aws as aws
import pulumi_synced_folder as synced_folder

path = "./www"
index_document = "index.html"
error_document = "404error.html"
website_name = "jeston.click"
www_name = f"www.{website_name}"
project_name = "jestonclick-"

# Imported zone
zone = aws.route53.Zone(
    f"{project_name}zone",
    name=website_name
)

# Bucket creation and management
main_bucket = aws.s3.Bucket(
    f"{project_name}main-bucket",
    bucket=website_name,
    website=aws.s3.BucketWebsiteArgs(
        index_document=index_document,
        error_document=error_document
    )
)
ownership_controls = aws.s3.BucketOwnershipControls(
    f"{project_name}ownership-controls",
    bucket=main_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="ObjectWriter"
    )
)
public_access_block = aws.s3.BucketPublicAccessBlock(
    f"{project_name}public_access_block",
    bucket=main_bucket.id,
    block_public_acls=False
)
bucket_folder = synced_folder.S3BucketFolder(
    f"{project_name}bucket-folder",
    acl="public-read",
    bucket_name=main_bucket.bucket,
    path=path,
    opts=pulumi.ResourceOptions(depends_on=[
        ownership_controls,
        public_access_block
    ])
)
www_bucket = aws.s3.Bucket(
    f"{project_name}www-bucket",
    bucket=www_name,
    website=aws.s3.BucketWebsiteArgs(
        redirect_all_requests_to=website_name
    )
)

# Certificate Creation
certificate = aws.acm.Certificate(
    f"{project_name}certificate",
    domain_name=website_name,
    subject_alternative_names=[www_name],
    validation_method="DNS"
)
cert_validation = aws.route53.Record(
    f"{project_name}cert-validation",
    name=certificate.domain_validation_options[0].resource_record_name,
    records=[certificate.domain_validation_options[0].resource_record_value],
    ttl=60,
    type=certificate.domain_validation_options[0].resource_record_type,
    zone_id=zone.id
)

# CDN Creation
main_cdn = aws.cloudfront.Distribution(
    f"{project_name}main-cdn",
    aliases=[website_name],
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
        acm_certificate_arn=certificate.arn,
        ssl_support_method="sni-only"
    ),
)
www_cdn = aws.cloudfront.Distribution(
    f"{project_name}www-cdn",
    aliases=[www_name],
    enabled=True,
    origins=[
        aws.cloudfront.DistributionOriginArgs(
            origin_id=www_bucket.arn,
            domain_name=www_bucket.website_endpoint,
            custom_origin_config=aws.cloudfront.DistributionOriginCustomOriginConfigArgs(
                origin_protocol_policy="http-only",
                http_port=80,
                https_port=443,
                origin_ssl_protocols=["TLSv1.2"],
            ),
        )
    ],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        target_origin_id=www_bucket.arn,
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
        acm_certificate_arn=certificate.arn,
        ssl_support_method="sni-only"
    ),
) 

# Records
main_record = aws.route53.Record(
    f"{project_name}main-record",
    zone_id=zone.id,
    name=website_name,
    type="A",
    aliases=[aws.route53.RecordAliasArgs(
        zone_id=main_cdn.hosted_zone_id,
        evaluate_target_health=True,
        name=main_cdn.domain_name
    )]
)
www_record = aws.route53.Record(
    f"{project_name}www-record",
    zone_id=zone.id,
    name=www_name,
    type="A",
    aliases=[aws.route53.RecordAliasArgs(
        zone_id=www_cdn.hosted_zone_id,
        evaluate_target_health=True,
        name=www_cdn.domain_name
    )]
)

# Create function
assume_role = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["lambda.amazonaws.com"]
            )],
            actions=["sts:AssumeRole"]
        )
    ]
)
iam_for_lambda = aws.iam.Role(
    f"{project_name}iamForLambda",
    assume_role_policy=assume_role.json,
)
lambda_basic_attach = aws.iam.RolePolicyAttachment(
    f"{project_name}lambdaBasicPolicyAttach",
    role=iam_for_lambda.name,
    policy_arn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)
ddb_policy_document = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=[
                "dynamodb:GetItem",
                "dynamodb:UpdateItem"
            ],
            resources=["*"]
        )
    ]
)
ddb_policy = aws.iam.Policy(
    f"{project_name}ddb-policy",
    description="lambda access to dynamodb",
    policy=ddb_policy_document.json
)
ddb_attach = aws.iam.RolePolicyAttachment(
    f"{project_name}dynamodbPolicyAttach",
    role=iam_for_lambda.name,
    policy_arn=ddb_policy.arn
)
count_lambda = archive.get_file(
    type="zip",
    source_file="page_count.py",
    output_path="lambda_count_payload.zip"
)
page_count = aws.lambda_.Function(
    f"{project_name}page-count",
    code=pulumi.FileArchive("lambda_count_payload.zip"),
    role=iam_for_lambda.arn,
    handler="page_count.handler",
    runtime="python3.9"
)

# Create api
apigw = aws.apigatewayv2.Api(
    f"{project_name}httpAPI", 
    protocol_type="HTTP",
    cors_configuration=aws.apigatewayv2.ApiCorsConfigurationArgs(
        allow_credentials=False,
        allow_headers=["*"],
        allow_methods=["*"],
        allow_origins=["*"],
        max_age=300
    )
)
integration = aws.apigatewayv2.Integration(
    f"{project_name}integration",
    api_id=apigw.id,
    integration_method="POST",
    integration_type="AWS_PROXY",
    integration_uri=page_count.arn,
    passthrough_behavior="WHEN_NO_MATCH",
    payload_format_version="2.0",
    timeout_milliseconds=30000
)
route = aws.apigatewayv2.Route(
    f"{project_name}route",
    api_id=apigw.id,
    route_key="GET /jestonclick-page-count-31ee36e",
    target="integrations/8wuggeg"
)
stage = aws.apigatewayv2.Stage(
    f"{project_name}stage",
    api_id=apigw.id,
    auto_deploy=True,
    name="prod"
)

# Create dynamo
ddb = aws.dynamodb.Table(
    f"{project_name}page-count-table",
    name="jestondotclick-page-views",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="pk",
            type="N"
        )
    ],
    hash_key="pk",
    billing_mode="PROVISIONED",
    read_capacity=5,
    write_capacity=5
)

# Outputs
pulumi.export(f"{project_name}cdnURL", pulumi.Output.concat("https://", main_cdn.domain_name))
pulumi.export(f"{project_name}pageCountName", page_count.name)
pulumi.export(f"{project_name}integrationID", integration.id)
pulumi.export(f"{project_name}lambdaInvokeURL", pulumi.Output.concat("https://",apigw.api_endpoint,page_count.name))
with open("./README.md") as f:
    pulumi.export("readme", f.read())