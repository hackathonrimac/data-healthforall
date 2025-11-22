#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-dev}"
AWS_PROFILE="${2:-hackathon}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_FILE="$ROOT_DIR/aws/backend.yml"
PARAMS_FILE="$ROOT_DIR/aws/params-${ENVIRONMENT}.json"
STACK_NAME="health-backend-${ENVIRONMENT}"
DIST_DIR="$ROOT_DIR/dist"

if [ ! -f "$PARAMS_FILE" ]; then
  echo "Parameters file $PARAMS_FILE not found" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to parse parameter files" >&2
  exit 1
fi

PARAM_OVERRIDES=$(jq -r 'to_entries | map("\(.key)=\(.value)") | join(" ")' "$PARAMS_FILE")
CODE_S3_BUCKET=$(jq -r '.CodeS3Bucket' "$PARAMS_FILE")
CODE_S3_KEY_PREFIX=$(jq -r '.CodeS3KeyPrefix // "backend"' "$PARAMS_FILE")

echo "==> Step 1: Packaging Lambda functions..."
bash "$ROOT_DIR/scripts/package_lambdas.sh"

echo "==> Step 2: Creating S3 bucket if it doesn't exist..."
if ! aws s3 ls "s3://${CODE_S3_BUCKET}" --profile "$AWS_PROFILE" >/dev/null 2>&1; then
  aws s3 mb "s3://${CODE_S3_BUCKET}" --profile "$AWS_PROFILE"
  echo "Created S3 bucket: ${CODE_S3_BUCKET}"
fi

echo "==> Step 3: Uploading Lambda packages to S3..."
for zip_file in "$DIST_DIR"/*.zip; do
  [ -f "$zip_file" ] || continue
  filename=$(basename "$zip_file")
  echo "Uploading ${filename} to s3://${CODE_S3_BUCKET}/${CODE_S3_KEY_PREFIX}/${filename}"
  aws s3 cp "$zip_file" "s3://${CODE_S3_BUCKET}/${CODE_S3_KEY_PREFIX}/${filename}" --profile "$AWS_PROFILE"
done

echo "==> Step 4: Deploying CloudFormation stack: $STACK_NAME"
aws cloudformation deploy \
  --template-file "$TEMPLATE_FILE" \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides $PARAM_OVERRIDES \
  --profile "$AWS_PROFILE"

echo "==> Deployment complete!"
