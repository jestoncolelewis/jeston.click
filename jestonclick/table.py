import builtins
from constructs import Construct
from aws_cdk import (
    aws_dynamodb as db
)

class Table(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = db.Table(
            self, "CountTable",
            table_name="jestondotclick-page-views",
            partition_key=db.Attribute(name="pk", type=db.AttributeType.NUMBER),
        )