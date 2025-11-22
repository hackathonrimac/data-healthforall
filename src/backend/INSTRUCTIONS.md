# Backend Deployment Instructions

## Prerequisites

- AWS CLI configured with profile `hackathon`
- Python 3.11+ installed
- `jq` command-line tool installed

## Quick Deploy (Recommended)

The deployment script automatically packages, uploads, and deploys:

```bash
cd /Users/raulescandon/Documents/hackathon-rimac/data-healthforall/src/backend

# Deploy to dev
bash scripts/deploy_backend.sh dev hackathon

# Deploy to prod
bash scripts/deploy_backend.sh prod hackathon
```

**What it does:**
1. Packages all Lambda functions into zip files
2. Creates S3 bucket if it doesn't exist
3. Uploads zip files to S3
4. Deploys CloudFormation stack

## Manual Steps (Advanced)

### Package Lambda functions only
```bash
bash scripts/package_lambdas.sh
```

### Upload artifacts to S3
```bash
# Dev environment
aws s3 sync dist/ s3://health-backend-artifacts-dev/dist/dev/ --profile hackathon

# Prod environment
aws s3 sync dist/ s3://health-backend-artifacts-prod/dist/prod/ --profile hackathon
```

## Troubleshooting

### Delete failed stack (ROLLBACK_COMPLETE state)
```bash
aws cloudformation delete-stack --stack-name health-backend-dev --profile hackathon

# Wait for deletion to complete
aws cloudformation wait stack-delete-complete --stack-name health-backend-dev --profile hackathon
```

### View stack events
```bash
aws cloudformation describe-stack-events --stack-name health-backend-dev --profile hackathon --max-items 20
```

### Verify S3 artifacts
```bash
aws s3 ls s3://health-backend-artifacts-dev/dist/dev/ --profile hackathon
```