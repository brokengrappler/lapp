from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lamda,
    aws_lambda_python_alpha as _alambda
)


class LappStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        initiator = _alambda.PythonFunction(
            self,
            "initiator",
            entry='./lambda/',
            runtime=Runtime.PYTHON_3_8,
            index='foo.py',
            handler='handle'
        )
