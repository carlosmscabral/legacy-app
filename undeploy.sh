#!/bin/bash
set -euo pipefail

: "${GCP_PROJECT_ID:?Please set GCP_PROJECT_ID environment variable}"
: "${GCP_REGION:?Please set GCP_REGION environment variable}"
: "${SERVICE_NAME:?Please set SERVICE_NAME environment variable}"

echo "INFO: Configuring gcloud CLI to use project '${GCP_PROJECT_ID}' and region '${GCP_REGION}'..."
gcloud config set project "${GCP_PROJECT_ID}"
gcloud config set run/region "${GCP_REGION}"
gcloud config set run/platform managed

echo "WARNING: This action will permanently delete the Cloud Run service '${SERVICE_NAME}' in project '${GCP_PROJECT_ID}' and region '${GCP_REGION}'."
read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Undeployment cancelled by user."
    exit 1
fi

echo "INFO: Proceeding with deletion of service '${SERVICE_NAME}'..."
gcloud run services delete "${SERVICE_NAME}" --quiet

echo "✅ SUCCESS: Service '${SERVICE_NAME}' has been deleted."
