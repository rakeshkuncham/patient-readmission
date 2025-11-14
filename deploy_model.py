import sagemaker
from sagemaker.model import Model
import time
import boto3

# Create SageMaker session
session = sagemaker.Session()
region = session.boto_region_name

# Your SageMaker execution role
role = "arn:aws:iam::626685033484:role/AmazonSageMaker-ExecutionRole"

# S3 location of the model.tar.gz
model_artifact = "s3://patient-risk-data-rakesh-2025/artifacts/readmission-risk-xgboost-20251113140026/output/model.tar.gz"

# Get SageMaker XGBoost container
image_uri = sagemaker.image_uris.retrieve(
    framework="xgboost",
    region=region,
    version="1.5-1"
)

# Create model
model = Model(
    image_uri=image_uri,
    model_data=model_artifact,
    role=role,
    sagemaker_session=session
)

# Create unique endpoint name
endpoint_name = f"readmission-risk-endpoint-{int(time.time())}"

print("Deploying endpoint:", endpoint_name)

# Deploy to SageMaker
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name=endpoint_name
)

print("Endpoint deployed:", endpoint_name)
