import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_sagemaker_custom_image.cdk_sagemaker_custom_image_stack import CdkSagemakerCustomImageStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_sagemaker_custom_image/cdk_sagemaker_custom_image_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSagemakerCustomImageStack(app, "cdk-sagemaker-custom-image")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
