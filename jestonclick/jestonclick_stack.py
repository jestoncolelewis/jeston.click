from constructs import Construct
from aws_cdk import (
    Stack
)
from .hosting import Hosting
from .counts import Counts

class JestonClickStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hosting = Hosting(self, "Hosting")
        form = Counts(self, "Form")
