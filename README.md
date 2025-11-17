<h1>Patient Readmission Risk Prediction</h1>


# Patient Readmission — Project README

> **One-stop guide** for the Patient Readmission Risk project (training, inference, API serving, frontend UI and deployment).

---

## Table of contents

1. Project overview
2. Repo structure
3. Prerequisites
4. Local setup (backend + model)
5. Training on SageMaker (steps & commands)
6. Deploying model to SageMaker endpoint
7. Serverless serving: Lambda + API Gateway
8. React frontend (development & build)
9. Add the UI folder into this repo (commands)
10. Deploy frontend (S3 + CloudFront) — quick guide
11. IAM policies and least-privilege notes
12. CI/CD recommendations (Jenkins/GitHub Actions)
13. Monitoring & cost controls
14. Troubleshooting checklist
15. Useful commands & references

---

## 1. Project overview

This repository contains an end-to-end pipeline for predicting patient readmission risk:

* **Data processing & training** (Python / scikit-learn / XGBoost / SageMaker)
* **Model training** on AWS SageMaker
* **Realtime inference** via a SageMaker endpoint
* **Serverless API** (API Gateway → Lambda) to expose predictions
* **React frontend** (Tailwind) to collect patient features and display risk

The goal: a reproducible pipeline that clinicians can use to get fast readmission risk predictions.

---

## 2. Repo structure (recommended)

```
patient-readmission/
├─ infra/                      # Terraform/CloudFormation (optional)
├─ training/                    # training scripts, train.py, data preprocessing
│  ├─ train.py
│  └─ preprocess.py
├─ sagemaker/                   # sagemaker launch & deploy helpers
│  ├─ run_training_job.py
│  └─ deploy_model.py
├─ lambda/                      # Lambda function code for inference
│  └─ readmission_lambda.py
├─ ui/ (or frontend/)           # React frontend built with Tailwind
│  ├─ package.json
│  └─ src/
├─ data/                        # (optional) sample datasets
├─ docs/                        # diagrams, architecture, screenshots
└─ README.md
```

---

## 3. Prerequisites

* **AWS account** with permissions to create SageMaker jobs, IAM roles, S3 buckets, Lambda and API Gateway.
* **AWS CLI** configured (`aws configure`) with a profile that has at least your user permissions for development.
* **Python 3.10+** (venv recommended)
* **Node.js & npm** (for React frontend)
* Optional: Terraform / CloudFormation if you want IaC.

Local tools to install:

```bash
# python tools
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows PowerShell
pip install -r training/requirements.txt

# node & frontend
cd ui
npm install
```

---

## 4. Local setup (backend & model)

1. Create and activate a Python virtual environment.
2. Install dependencies (example `requirements.txt` should include `boto3`, `sagemaker`, `xgboost`, `pandas`, `scikit-learn`).
3. Prepare your S3 bucket and upload processed train/validation CSVs:

```bash
aws s3 mb s3://patient-risk-data-<your-suffix> --region us-east-1
aws s3 cp data/processed/train.csv s3://patient-risk-data-<your-suffix>/processed/train.csv
aws s3 cp data/processed/validation.csv s3://patient-risk-data-<your-suffix>/processed/validation.csv
```

4. Edit `run_training_job.py` and set your bucket name, role ARN, region and job name.

---

## 5. Training on SageMaker

Use the provided `run_training_job.py` to launch a training job.

```bash
python run_training_job.py
```

What it does:

* Creates a SageMaker session
* Configures an Estimator (XGBoost or PyTorch depending on script)
* Submits the training job (model artifacts are saved to S3)

**Verify** the training job in the SageMaker Console → Training jobs. When it completes, note the `ModelArtifacts.S3ModelArtifacts` path (e.g. `s3://.../output/model.tar.gz`).

---

## 6. Deploying the model to a SageMaker endpoint

Use `deploy_model.py` (or `sagemaker.xgboost.XGBoostModel`) to create a Model and deploy to an endpoint.

Example (from this repo):

```bash
python deploy_model.py
```

Key notes:

* Ensure the `role` used is an **IAM role** (e.g. `arn:aws:iam::ACCOUNT:role/AmazonSageMaker-ExecutionRole`) — not an IAM user.
* The role must have `s3:GetObject` and `s3:ListBucket` permissions for the model bucket and `sts:AssumeRole` trust for `sagemaker.amazonaws.com`.
* If the endpoint fails health checks, check CloudWatch logs for the endpoint, verify the model.tar.gz contents and that you used the correct container image (XGBoost built-in or custom).

---

## 7. Serverless serving (Lambda + API Gateway)

High-level flow: Frontend → API Gateway → Lambda → SageMaker Runtime → SageMaker Endpoint → Lambda returns prediction.

### Lambda handler (Python 3.12) example

```py
import json
import boto3

runtime = boto3.client('sagemaker-runtime')
ENDPOINT_NAME = "readmission-risk-endpoint-..."

def lambda_handler(event, context):
    # Support both proxy and direct JSON
    if 'body' in event:
        payload = json.loads(event['body'])
    else:
        payload = event

    csv_input = payload['input']

    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='text/csv',
        Body=csv_input
    )

    prediction = response['Body'].read().decode('utf-8')

    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': prediction})
    }
```

### API Gateway

* Create `/predict` resource and **POST** method integrated with your Lambda function (use Lambda Proxy integration).
* Enable CORS for your frontend domain.
* Deploy to stage (e.g., `prod`) and copy the invoke URL.

Test with `curl` or Postman (POST):

```bash
curl -X POST https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/predict \
 -H "Content-Type: application/json" \
 -d '{"body":"{\"input\":\"45,0,1,100,5,120,3\"}"}'
```

Troubleshooting API Gateway:

* `Missing Authentication Token` usually means the path or method is not deployed or wrong HTTP verb used.
* If you get 500 from Lambda, look at CloudWatch Logs for the Lambda function.

---

## 8. React frontend — development & build

Project assumes a `ui/` folder inside the repo created with `create-react-app` and Tailwind.

### Run locally

```bash
cd ui
npm install
npm start
```

### Build for production

```bash
npm run build
```

Your built static files will be in `ui/build/`.

The frontend expects the API to accept POST requests at `/predict`. Example payload (frontend uses this wrapper):

```json
{ "body": "{\"input\": \"45,0,1,100,5,120,3\"}" }
```

### Important files

* `src/components/PatientForm.js` — collects inputs and calls the API
* `src/components/ResultCard.js` — displays prediction
* `src/pages/Dashboard.js` — layout

---

## 9. Add UI folder into this repo (safe method)

If you already created the UI project separately, move it into the main repo:

```bash
# from repo root
mv ../patient-readmission-ui ./ui       # linux/mac
move ..\patient-readmission-ui .\ui   # windows

# then commit
git add ui
git commit -m "Add React frontend (ui/)"
git push origin main
```

If you prefer the UI in `frontend/` or `webapp/`, rename accordingly.

---

## 10. Deploy frontend (S3 + CloudFront) — quick guide

1. Create S3 bucket (static website hosting) and enable public read (or use CloudFront with OAI).
2. Upload `ui/build/` contents.
3. Create a CloudFront distribution pointing to the S3 bucket.
4. Configure HTTPS with ACM and set the domain.

Commands (CLI):

```bash
aws s3 sync ui/build/ s3://<bucket-name>/ --delete
```

Use CloudFront for best performance and HTTPS.

---

## 11. IAM policies — minimum privileges examples

### SageMaker execution role (model access)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "sagemaker.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Attach to the role a policy with:

* `s3:GetObject`, `s3:ListBucket` for the model bucket
* `logs:CreateLogGroup` / `logs:CreateLogStream` / `logs:PutLogEvents` (if you want CloudWatch logs)

### Lambda execution role

Attach:

* `AmazonSageMakerFullAccess` (or fine-grained: `sagemaker:InvokeEndpoint`)
* `CloudWatchLogsFullAccess`
* `AmazonS3ReadOnlyAccess` (if reading inputs from S3)

---

## 12. CI/CD recommendations

* **Jenkins / GitHub Actions** to automate:

  * Unit tests
  * Build Docker images (if custom container)
  * Push artifacts to ECR / S3
  * Trigger SageMaker training via SDK or CloudFormation
  * Deploy frontend to S3 or Netlify

* **Model registry**: use SageMaker Model Registry or store model metadata in a small DB (DynamoDB) to track versions.

---

## 13. Monitoring & cost controls

* Use CloudWatch to monitor endpoint invocation metrics and Lambda errors.
* Set CloudWatch alarms for high latency or error rates.
* Use SageMaker endpoint autoscaling or multi-model endpoints to reduce cost.
* If cost is a concern, switch to asynchronous inference or batch transform instead of real-time endpoints.

---

## 14. Troubleshooting checklist

* `Missing Authentication Token` → wrong URL, method not deployed or calling GET instead of POST.
* `AccessDenied` when creating job/endpoint → IAM policy missing actions (attach correct policies).
* `Container did not pass health check` → wrong container image, missing entry_point, or model artifact mismatch.
* `Could not access model data` → ensure execution role has `s3:GetObject` for model bucket & same region.
* If Lambda returns 500 → check CloudWatch logs for stack trace.

---

## 15. Useful commands & references

**AWS CLI**

```bash
aws sts get-caller-identity
aws s3 ls s3://patient-risk-data-<suffix>/artifacts/
```

**SageMaker SDK docs**: [https://sagemaker.readthedocs.io/](https://sagemaker.readthedocs.io/)

**API Gateway docs**: [https://docs.aws.amazon.com/apigateway/](https://docs.aws.amazon.com/apigateway/)

**React + Tailwind guide**: [https://tailwindcss.com/docs/guides/create-react-app](https://tailwindcss.com/docs/guides/create-react-app)

---

## Contact / Author

**Rakesh Kuncham** — [rakeshkuncham777@gmail.com](mailto:rakeshkuncham777@gmail.com)

---





OUTPUT ------
<img width="1920" height="1080" alt="Screenshot (367)" src="https://github.com/user-attachments/assets/22efa2f2-f688-4aaf-9f1f-7cc6c38a1408" />

