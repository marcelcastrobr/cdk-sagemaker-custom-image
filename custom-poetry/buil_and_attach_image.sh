#/bin/bash

# Modify these as required. The Docker registry endpoint can be tuned based on your current region from https://docs.aws.amazon.com/general/latest/gr/ecr.html#ecr-docker-endpoints
REGION=eu-west-1
ACCOUNT_ID=$(aws sts get-caller-identity | jq -r '.Account') 
IMAGE_NAME=custom-poetry-kernel

echo "ACCOUNT_ID=${ACCOUNT_ID}"
echo "REGION=${REGION}"
echo "IMAGE_NAME=${IMAGE_NAME}"


# Create ECR Repository. Ignore if it exists. For simplcity, all examples in the repo
# use same ECR repo with different image tags
#aws --region ${REGION} ecr create-repository --repository-name smstudio-custom

# Build the image
#aws --region ${REGION} ecr get-login-password | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/smstudio-custom

echo "Building Image!!!"
#docker build . -t ${IMAGE_NAME} -t ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/smstudio-custom:${IMAGE_NAME} --platform=linux/amd64

echo "Pushing Image!!!"
#docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/smstudio-custom:${IMAGE_NAME}

echo "Using it with SageMaker Studio"
# Role in your account to be used for the SageMaker Image
ROLE_ARN=arn:aws:iam::656001362760:role/service-role/AmazonSageMaker-ExecutionRole-20220811T111858

#aws --region ${REGION} sagemaker create-image \
#    --image-name ${IMAGE_NAME} \
#    --role-arn ${ROLE_ARN}

aws --region ${REGION} sagemaker create-image-version \
    --image-name ${IMAGE_NAME} \
    --base-image "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/smstudio-custom:${IMAGE_NAME}"

# Verify the image-version is created successfully. Do NOT proceed if image-version is in CREATE_FAILED state or in any other state apart from CREATED.
IMAGE_VERSION=$(aws --region ${REGION} sagemaker describe-image-version --image-name ${IMAGE_NAME}| jq -r '.Version')
echo "IMAGE_VERSION=$IMAGE_VERSION"

echo "Create an AppImageConfig for this image."
aws --region ${REGION} sagemaker delete-app-image-config \
    --app-image-config-name custom-poetry-kernel-image-config
sed 's/<image-version>/'"$IMAGE_VERSION"'/' app-image-config-input.json > app-image-config-input-mod.json
aws --region ${REGION} sagemaker create-app-image-config \
    --cli-input-json file://app-image-config-input-mod.json

echo "Update SageMaker Domain"
# inject your DOMAIN_ID into the configuration file
sed 's/<domain-id>/'"$DOMAIN_ID"'/' update-domain-input.json > update-domain-input-mod.json
aws --region ${REGION} sagemaker update-domain --cli-input-json file://update-domain-input-mod.json