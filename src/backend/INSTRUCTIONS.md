# Backend Deployment Instructions

## Prerequisites

- AWS CLI configured with profile `hackathon`
- Python 3.11+ installed
- `jq` command-line tool installed

## Quick Deploy (Recommended)

### Full Deployment (Lambdas + Infrastructure)

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
4. Deploys/updates CloudFormation stack
5. Displays API endpoint URLs

### CloudFormation Only (Infrastructure Changes)

Use this when you only need to update infrastructure (e.g., API Gateway, IAM, DynamoDB schema) without modifying Lambda code:

```bash
# Deploy to dev (CloudFormation only)
bash scripts/deploy_backend.sh dev hackathon --skip-lambdas

# Deploy to prod (CloudFormation only)
bash scripts/deploy_backend.sh prod hackathon --skip-lambdas
```

**What it does:**
1. ✅ Updates CloudFormation stack (API Gateway, IAM, etc.)
2. ✅ Displays API endpoint URLs
3. ❌ Skips Lambda packaging and uploading
4. ❌ Does NOT modify DynamoDB table data

**When to use `--skip-lambdas`:**
- Updating API Gateway configuration
- Modifying IAM permissions
- Adding/removing CloudFormation outputs
- Any infrastructure change that doesn't require new Lambda code

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

## View API Endpoints

After deployment, view all available API endpoints:

```bash
# Dev environment
aws cloudformation describe-stacks \
  --stack-name health-backend-dev \
  --query 'Stacks[0].Outputs' \
  --output table \
  --profile hackathon

# Prod environment
aws cloudformation describe-stacks \
  --stack-name health-backend-prod \
  --query 'Stacks[0].Outputs' \
  --output table \
  --profile hackathon
```

**Available endpoints:**
- `ApiBaseUrl` - Base URL for all endpoints
- `ClinicsEndpoint` - GET /clinics
- `DoctorsEndpoint` - GET /doctors
- `EspecialidadesEndpoint` - GET /especialidades
- `SubEspecialidadesEndpoint` - GET /subespecialidades
- `SegurosEndpoint` - GET /seguros
- `SegurosClinicasEndpoint` - GET /seguros-clinicas
- `SearchDoctorsEndpoint` - GET /search/doctors

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