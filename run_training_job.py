import sagemaker
import boto3
from sagemaker import Session
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
import os
import logging
from datetime import datetime

# --- LOGGING CONFIG ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION ---
SAGEMAKER_EXECUTION_ROLE_ARN = 'arn:aws:iam::626685033484:role/SageMakerExecutionRole'
BUCKET_NAME = 'patient-risk-data-rakesh-2025'
REGION = 'us-east-1'
DATA_PREFIX = 'processed'
OUTPUT_PREFIX = 'artifacts'
INSTANCE_TYPE = 'ml.m5.large'
SCRIPT_PATH = 'train.py'
TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
JOB_NAME = f'readmission-risk-xgboost-{TIMESTAMP}'
# ---------------------

def launch_training_job():
    logging.info("Starting SageMaker session and configuration...")

    # Create boto3 + SageMaker session
    boto_session = boto3.Session(region_name=REGION)
    sagemaker_session = sagemaker.Session(boto_session=boto_session)

    # XGBoost built-in container (you don’t need to provide train.py for built-in)
    framework_version = '1.7-1'  # XGBoost version in SageMaker

    logging.info(f"Configuring XGBoost Estimator for job: {JOB_NAME}")

    # Define the SageMaker XGBoost Estimator
    xgb_image_uri = sagemaker.image_uris.retrieve(
        framework='xgboost',
        region=REGION,
        version=framework_version
    )

    estimator = Estimator(
        image_uri=xgb_image_uri,
        role=SAGEMAKER_EXECUTION_ROLE_ARN,
        instance_count=1,
        instance_type=INSTANCE_TYPE,
        volume_size=10,
        max_run=3600,
        output_path=f's3://{BUCKET_NAME}/{OUTPUT_PREFIX}',
        sagemaker_session=sagemaker_session,
        hyperparameters={
            'num_round': 100,
            'eta': 0.1,
            'max_depth': 5,
            'subsample': 0.8,
            'objective': 'binary:logistic',
            'eval_metric': 'auc'
        }
    )

    # Define S3 data input paths
    s3_train_data = f's3://{BUCKET_NAME}/{DATA_PREFIX}/train.csv'
    s3_validation_data = f's3://{BUCKET_NAME}/{DATA_PREFIX}/validation.csv'

    inputs = {
        'train': TrainingInput(s3_train_data, content_type='text/csv'),
        'validation': TrainingInput(s3_validation_data, content_type='text/csv')
    }

    # Launch training job
    logging.info(f"Submitting SageMaker training job: {JOB_NAME}")
    estimator.fit(inputs, job_name=JOB_NAME, wait=False)

    logging.info("✅ Training job submitted successfully!")
    logging.info(f"Check progress in SageMaker Console > Training Jobs")
    logging.info(f"Job Name: {JOB_NAME}")

    return JOB_NAME


if __name__ == '__main__':
    try:
        import boto3
    except ImportError:
        print("Boto3 is required. Please install it: pip install boto3")
        exit(1)

    launch_training_job()
