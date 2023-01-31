import aws_cdk as cdk
from constructs import Construct
from aws_cdk import(
    Stack,
    pipelines as pipelines,
)
import aws_cdk.aws_secretsmanager as secretsmanager
import aws_cdk.aws_iam as iam

class MyPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  pipelines.CodePipeline(self, "Pipeline",
                        synth=pipelines.ShellStep("Synth", 
                            input=pipelines.CodePipelineSource.connection("marcelcastrobr/cdk-sagemaker-custom-image", "main",
                                connection_arn='arn:aws:codestar-connections:eu-west-1:656001362760:connection/2a1bfdaa-d478-45c4-97e7-9421595608b4'
                                ),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )