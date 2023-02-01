#/bin/python
import boto3

REGION=eu-west-1
ACCOUNT_ID=656001362760
IMAGE_NAME='custom-poetry-kernel'

tag = ':latest'
account_id = boto3.client('sts').get_caller_identity().get('Account')
region = boto3.Session().region_name
ecr_repository = 'specrec-sagemaker-cdk'

image_uri = '{}.dkr.ecr.{}.amazonaws.com/{}'.format(account_id, region, ecr_repository + tag)

print(f'My image in ECR is: {image_uri}')

# Build docker image
# docker build -t image_uri docker