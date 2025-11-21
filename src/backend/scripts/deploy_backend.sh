#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-dev}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_FILE="$ROOT_DIR/aws/backend.yml"
PARAMS_FILE="$ROOT_DIR/aws/params-${ENVIRONMENT}.json"
STACK_NAME="health-backend-${ENVIRONMENT}"

if [ ! -f "$PARAMS_FILE" ]; then
  echo "Parameters file $PARAMS_FILE not found" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to parse parameter files" >&2
  exit 1
fi

PARAM_OVERRIDES=$(jq -r 'to_entries | map("\(.key)=\(.value)") | join(" ")' "$PARAMS_FILE")

aws cloudformation deploy \
  --template-file "$TEMPLATE_FILE" \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides $PARAM_OVERRIDES
