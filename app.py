#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_sagemaker_custom_image.cdk_sagemaker_custom_image_stack import MyCustomImageStack


PIPELINE_ACCOUNT = '656001362760'
#DOMAIN_ID = 'd-vpxb1borhdps'
domain_id = os.environ.get('DOMAIN_ID', None)

app = cdk.App()
MyCustomImageStack(app, 
    "MyPipelineStack", 
    domain_id,
    env={
        'account': PIPELINE_ACCOUNT,
        'region': 'eu-west-1'
    }
)

app.synth()