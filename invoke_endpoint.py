import boto3
import json

endpoint_name = "readmission-risk-endpoint-1763103664"

runtime = boto3.client("sagemaker-runtime")

# Example input (replace with real features)
data = "0.12,0.75,45,1,0,3"

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=data
)

print("Prediction:", response["Body"].read().decode())
