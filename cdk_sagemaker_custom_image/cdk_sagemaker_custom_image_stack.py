import aws_cdk as cdk
from constructs import Construct
from aws_cdk import(
    Stack,
    pipelines as pipelines,
    aws_sagemaker as sagemaker,
)
import aws_cdk.aws_sagemaker_alpha as sagemaker_alpha
from os import path
import aws_cdk.aws_secretsmanager as secretsmanager
import aws_cdk.aws_iam as iam

class MyCustomImageStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        this_dir = path.dirname(__file__)
        # Using sagemaker
        '''
        # Using sagemaker_alpha
        image = sagemaker_alpha.ContainerImage.from_asset(path.join(this_dir,'../custom-poetry'))
        model_data = sagemaker_alpha.ModelData.from_asset(path.join(this_dir,'../model/file.tar.gz'))

        model = sagemaker_alpha.Model(self, "PrimaryContainerModel",
            containers=[sagemaker_alpha.ContainerDefinition(
                image=image,
                model_data=model_data
            )
            ]
        )
        '''

        if domain_id is not None:
            print("Doing things!!!")
        
            ##########
            # Custom SageMaker image (https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi-create.html?icmpid=docs_sagemaker_console_studio)
            ##########

            # Create a SageMaker Image (SMI) with the image in ECR.
            cfn_image = sagemaker.CfnImage(
                self, 
                "MyCfnImage",
                image_name="custom-poetry-kernel-v3",
                image_role_arn="arn:aws:iam::656001362760:role/service-role/AmazonCodeBuild-ServiceRole-CustomImage",
            )

            cfn_image_version = sagemaker.CfnImageVersion(
                self, 
                "MyCfnImageVersion",
                base_image="656001362760.dkr.ecr.eu-west-1.amazonaws.com/smstudio-custom:custom-poetry-kernel-v2",
                image_name="custom-poetry-kernel-v2"
            )
            print(cfn_image_version.image_name)
            
            cfn_image_version.add_depends_on(cfn_image)
            
            # Create an AppImageConfig for this image.
            cfn_app_image_config = sagemaker.CfnAppImageConfig(
                self,
                "DvcAppImageConfig",
                app_image_config_name="cdk-conda-env-dvc-kernel-config",
                kernel_gateway_image_config=sagemaker.CfnAppImageConfig.KernelGatewayImageConfigProperty(
                    kernel_specs=[
                        sagemaker.CfnAppImageConfig.KernelSpecProperty(
                            name="conda-env-dvc-py",
                            display_name="Python [conda env: dvc]"
                        )
                    ],
                    file_system_config=sagemaker.CfnAppImageConfig.FileSystemConfigProperty(
                        default_gid=0,
                        default_uid=0,
                        mount_path="/root"
                    )
                ),
            )
            cfn_app_image_config.add_depends_on(cfn_image_version)

            # Attach a custom SageMaker image to a domain.

        else:
            print("Doing Nothing: I do not have a domain!!!")







        

        