# Infrastructure as Code - Terraform AWS

This directory contains Terraform configurations for deploying the Python applications to AWS.

## Overview

The Terraform configuration creates the following AWS resources:

- **VPC**: Virtual Private Cloud with public and private subnets across 2 AZs
- **RDS PostgreSQL**: Managed relational database
- **ElastiCache Redis**: Managed in-memory caching service
- **Security Groups**: Network access control for all resources
- **IAM Roles**: Permissions for RDS monitoring
- **Networking**: NAT Gateways, Internet Gateway, Route Tables
- **Encryption**: KMS keys for RDS encryption
- **Monitoring**: CloudWatch Logs for Redis slow-log

## Prerequisites

1. AWS Account
2. Terraform >= 1.0
3. AWS CLI configured with credentials
4. S3 bucket and DynamoDB table for state management

## File Structure

```
terraform/
├── main.tf              # Main configuration and state setup
├── variables.tf         # Input variables
├── vpc.tf              # VPC and networking
├── rds.tf              # PostgreSQL database
├── redis.tf            # ElastiCache Redis
├── outputs.tf          # Output values
├── development.tfvars  # Development environment variables
├── staging.tfvars      # Staging environment variables
├── production.tfvars   # Production environment variables
└── README.md           # This file
```

## Usage

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Plan the Infrastructure

```bash
# For development
terraform plan -var-file=development.tfvars -out=tfplan

# For staging
terraform plan -var-file=staging.tfvars -out=tfplan

# For production
terraform plan -var-file=production.tfvars -out=tfplan
```

### 3. Apply the Configuration

```bash
# Apply the saved plan
terraform apply tfplan
```

### 4. Get Outputs

```bash
# Display all outputs
terraform output

# Get specific output
terraform output rds_endpoint
terraform output redis_endpoint
```

## Variables

Key variables that can be customized:

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region | us-east-1 |
| `environment` | Environment name | production |
| `vpc_cidr` | VPC CIDR block | 10.0.0.0/16 |
| `instance_type` | EC2 instance type | t3.medium |
| `db_instance_class` | RDS instance class | db.t3.micro |
| `db_allocated_storage` | RDS storage in GB | 20 |
| `db_username` | RDS username | admin |
| `db_password` | RDS password | (required) |
| `redis_node_type` | ElastiCache node type | cache.t3.micro |

## Environment-Specific Configuration

Use the appropriate .tfvars file for each environment:

```bash
# Development
terraform apply -var-file=development.tfvars

# Staging
terraform apply -var-file=staging.tfvars

# Production
terraform apply -var-file=production.tfvars
```

## State Management

Terraform state is stored in S3 with:
- Encryption enabled
- Versioning enabled
- DynamoDB table for state locking

## Security

- RDS encryption with KMS
- Redis auth token and encryption
- Security groups for network isolation
- IAM roles with least privilege
- No public database access

## Cost Estimation

To estimate costs:

```bash
terraform plan -var-file=development.tfvars -json | terraform cost estimate
```

Or use AWS Cost Explorer for detailed estimates.

## Destroying Resources

**Warning**: This will delete all resources including the database.

```bash
# Destroy with confirmation prompt
terraform destroy -var-file=environment.tfvars

# Destroy without confirmation
terraform destroy -var-file=environment.tfvars -auto-approve
```

## Troubleshooting

### Authentication Issues

Ensure AWS credentials are configured:

```bash
aws configure
```

### State Lock

If state is locked:

```bash
terraform force-unlock <lock_id>
```

### Plan Differences

To see what changed:

```bash
terraform plan -refresh-only
```

## Advanced Usage

### Adding New Resources

1. Create a new .tf file (e.g., `alb.tf`)
2. Define resources
3. Add outputs
4. Run `terraform plan` and `terraform apply`

### Updating RDS

```bash
terraform apply -var-file=production.tfvars -target=aws_db_instance.main
```

### Scaling Redis

Update `redis_num_cache_clusters` in the .tfvars file:

```bash
terraform apply -var-file=production.tfvars -target=aws_elasticache_cluster.main
```

## Monitoring

CloudWatch metrics and logs are automatically configured:

- RDS performance metrics
- Redis slow-log entries
- VPC Flow Logs

## Backup and Recovery

### RDS Snapshots

Automated backups are configured with retention:
- Development: 7 days
- Production: 30 days

Manual backup:

```bash
aws rds create-db-snapshot --db-instance-identifier python-apps-db --db-snapshot-identifier backup-$(date +%s)
```

## Migration from Manual Setup

If you had manual AWS resources:

1. Import them into Terraform state
2. Update configuration to match resources
3. Use `terraform import`

## Support

For issues or questions, check:
- Terraform AWS Provider docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- AWS documentation
- Terraform documentation

## License

MIT
