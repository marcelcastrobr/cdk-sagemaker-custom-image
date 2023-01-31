#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_sagemaker_custom_image.cdk_sagemaker_custom_image_stack import MyPipelineStack

PIPELINE_ACCOUNT = '656001362760'

app = cdk.App()
MyPipelineStack(app, "MyPipelineStack", 
    env={
        'account': PIPELINE_ACCOUNT,
        'region': 'eu-west-1'
    }
)

app.synth()