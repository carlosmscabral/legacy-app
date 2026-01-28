#!/bin/bash
set -euo pipefail

: "${GCP_PROJECT_ID:?Please set GCP_PROJECT_ID environment variable}"
: "${GCP_REGION:?Please set GCP_REGION environment variable}"
: "${SERVICE_NAME:?Please set SERVICE_NAME environment variable}"

echo "INFO: Configuring gcloud CLI to use project '${GCP_PROJECT_ID}' and region '${GCP_REGION}'..."
gcloud config set project "${GCP_PROJECT_ID}"
gcloud config set run/region "${GCP_REGION}"
gcloud config set run/platform managed

echo "INFO: Starting deployment of service '${SERVICE_NAME}' to region '${GCP_REGION}'..."

gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --allow-unauthenticated \
  --quiet

SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --format 'value(status.url)')

echo "✅ SUCCESS: Deployment of '${SERVICE_NAME}' is complete."
echo "   Service is available at: ${SERVICE_URL}"
