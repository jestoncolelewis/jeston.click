from constructs import Construct
from aws_cdk import (
    aws_route53 as r53,
    aws_route53_targets as targets,
    aws_ses as ses,
    RemovalPolicy
)
from s_front_end.buckets import Buckets, name

class Hosting(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        @property
        def zone(self):
            return self._zone

        # Hosting
        hosted_zone = r53.HostedZone.from_hosted_zone_attributes(
            self, 'HostedZone',
            hosted_zone_id="Z02591293JOU7GDHXDA3Y",
            zone_name=name
        )

        bucket = Buckets(self, 'Buckets')

        main_record = r53.RecordSet(
            self, 'MainRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.CloudFrontTarget(bucket._main_distro)),
            zone=hosted_zone,
            record_name=name
        )

        www_record = r53.RecordSet(
            self, 'wwwRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.CloudFrontTarget(bucket._www_distro)),
            zone=hosted_zone,
            record_name='www.' + name
        )

        identity = ses.EmailIdentity(
            self, "Identity",
            identity=ses.Identity.public_hosted_zone(hosted_zone),
            mail_from_domain="mail." + name
        )

        # hosted_zone.apply_removal_policy(RemovalPolicy.RETAIN)

        self._zone = hosted_zone