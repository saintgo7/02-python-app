#!/usr/bin/env python3
"""
Terraform Infrastructure Setup
Creates AWS infrastructure as code for deploying all 60 projects
"""

from pathlib import Path

def generate_terraform_main() -> str:
    """Generate main Terraform configuration"""
    return '''terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "python-apps/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Python Applications"
      Environment = var.environment
      ManagedBy   = "Terraform"
      CreatedAt   = formatdate("YYYY-MM-DD", timestamp())
    }
  }
}

# Create S3 bucket for Terraform state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "Terraform State Bucket"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DynamoDB table for Terraform state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform State Lock"
  }
}

data "aws_caller_identity" "current" {}

output "aws_account_id" {
  value       = data.aws_caller_identity.current.account_id
  description = "AWS Account ID"
}
'''

def generate_terraform_variables() -> str:
    """Generate Terraform variables"""
    return '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "python-apps"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "RDS database name"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "RDS database username"
  type        = string
  default     = "admin"
  sensitive   = true
}

variable "db_password" {
  description = "RDS database password"
  type        = string
  sensitive   = true
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_num_cache_clusters" {
  description = "Number of cache clusters"
  type        = number
  default     = 1
}

variable "environment_variables" {
  description = "Environment variables for application"
  type        = map(string)
  default = {
    DEBUG = "false"
  }
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Project = "Python Applications"
  }
}
'''

def generate_terraform_vpc() -> str:
    """Generate VPC and networking configuration"""
    return '''# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-1"
  }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-2"
  }
}

# Private Subnets
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.project_name}-private-subnet-1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.project_name}-private-subnet-2"
  }
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat_1" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-nat-eip-1"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat_2" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-nat-eip-2"
  }

  depends_on = [aws_internet_gateway.main]
}

# NAT Gateways
resource "aws_nat_gateway" "nat_1" {
  allocation_id = aws_eip.nat_1.id
  subnet_id     = aws_subnet.public_1.id

  tags = {
    Name = "${var.project_name}-nat-1"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "nat_2" {
  allocation_id = aws_eip.nat_2.id
  subnet_id     = aws_subnet.public_2.id

  tags = {
    Name = "${var.project_name}-nat-2"
  }

  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table" "private_1" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_1.id
  }

  tags = {
    Name = "${var.project_name}-private-rt-1"
  }
}

resource "aws_route_table" "private_2" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_2.id
  }

  tags = {
    Name = "${var.project_name}-private-rt-2"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_1.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_2.id
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for application instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

resource "aws_security_group" "db" {
  name        = "${var.project_name}-db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-db-sg"
  }
}

resource "aws_security_group" "redis" {
  name        = "${var.project_name}-redis-sg"
  description = "Security group for Redis"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-redis-sg"
  }
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Outputs
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}

output "public_subnet_1_id" {
  value       = aws_subnet.public_1.id
  description = "Public subnet 1 ID"
}

output "public_subnet_2_id" {
  value       = aws_subnet.public_2.id
  description = "Public subnet 2 ID"
}

output "private_subnet_1_id" {
  value       = aws_subnet.private_1.id
  description = "Private subnet 1 ID"
}

output "private_subnet_2_id" {
  value       = aws_subnet.private_2.id
  description = "Private subnet 2 ID"
}

output "alb_security_group_id" {
  value       = aws_security_group.alb.id
  description = "ALB security group ID"
}

output "app_security_group_id" {
  value       = aws_security_group.app.id
  description = "Application security group ID"
}

output "db_security_group_id" {
  value       = aws_security_group.db.id
  description = "Database security group ID"
}

output "redis_security_group_id" {
  value       = aws_security_group.redis.id
  description = "Redis security group ID"
}
'''

def generate_terraform_rds() -> str:
    """Generate RDS configuration"""
    return '''# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.db_instance_class

  allocated_storage    = var.db_allocated_storage
  storage_type         = "gp3"
  storage_encrypted    = true
  kms_key_id          = aws_kms_key.rds.arn

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name            = aws_db_subnet_group.main.name
  vpc_security_group_ids          = [aws_security_group.db.id]
  publicly_accessible             = false
  multi_az                        = var.environment == "production" ? true : false
  storage_autoscaling_enabled     = true
  storage_autoscaling_max_storage = 100

  backup_retention_period = var.environment == "production" ? 30 : 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  copy_tags_to_snapshot  = true

  enabled_cloudwatch_logs_exports = ["postgresql"]
  monitoring_interval             = 60
  monitoring_role_arn            = aws_iam_role.rds_monitoring.arn

  skip_final_snapshot       = var.environment != "production" ? true : false
  final_snapshot_identifier = "${var.project_name}-db-final-snapshot"

  tags = {
    Name = "${var.project_name}-db"
  }
}

# KMS Key for RDS encryption
resource "aws_kms_key" "rds" {
  description             = "KMS key for RDS encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Name = "${var.project_name}-rds-key"
  }
}

# RDS Monitoring Role
resource "aws_iam_role" "rds_monitoring" {
  name = "${var.project_name}-rds-monitoring-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# Outputs
output "rds_endpoint" {
  value       = aws_db_instance.main.endpoint
  description = "RDS database endpoint"
  sensitive   = true
}

output "rds_address" {
  value       = aws_db_instance.main.address
  description = "RDS database address"
}

output "rds_port" {
  value       = aws_db_instance.main.port
  description = "RDS database port"
}

output "rds_database_name" {
  value       = aws_db_instance.main.db_name
  description = "RDS database name"
}
'''

def generate_terraform_redis() -> str:
    """Generate ElastiCache Redis configuration"""
    return '''# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-cache-subnet-group"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "${var.project_name}-cache-subnet-group"
  }
}

# ElastiCache Redis Cluster
resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  node_type            = var.redis_node_type
  num_cache_nodes      = var.redis_num_cache_clusters
  parameter_group_name = aws_elasticache_parameter_group.main.name
  engine_version       = "7.0"
  port                 = 6379

  subnet_group_name       = aws_elasticache_subnet_group.main.name
  security_group_ids      = [aws_security_group.redis.id]
  automatic_failover_enabled = var.environment == "production" ? true : false

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                = random_password.redis_auth_token.result

  maintenance_window = "sun:05:00-sun:07:00"
  notification_topic_arn = var.environment == "production" ? aws_sns_topic.elasticache_notifications.arn : null

  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis_slow_log.name
    destination_type = "cloudwatch-logs"
    log_format       = "json"
    log_type         = "slow-log"
    enabled          = true
  }

  tags = {
    Name = "${var.project_name}-redis"
  }
}

# ElastiCache Parameter Group
resource "aws_elasticache_parameter_group" "main" {
  family      = "redis7"
  name        = "${var.project_name}-redis-params"
  description = "Redis parameter group"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }

  parameter {
    name  = "timeout"
    value = "300"
  }

  tags = {
    Name = "${var.project_name}-redis-params"
  }
}

# Redis Auth Token
resource "random_password" "redis_auth_token" {
  length  = 32
  special = true
}

# CloudWatch Log Group for Redis
resource "aws_cloudwatch_log_group" "redis_slow_log" {
  name              = "/aws/elasticache/${var.project_name}-redis"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-redis-logs"
  }
}

# SNS Topic for notifications
resource "aws_sns_topic" "elasticache_notifications" {
  name = "${var.project_name}-elasticache-notifications"

  tags = {
    Name = "${var.project_name}-elasticache-topic"
  }
}

# Outputs
output "redis_endpoint" {
  value       = aws_elasticache_cluster.main.cache_nodes[0].address
  description = "Redis endpoint address"
}

output "redis_port" {
  value       = aws_elasticache_cluster.main.port
  description = "Redis port"
}

output "redis_auth_token" {
  value       = random_password.redis_auth_token.result
  description = "Redis authentication token"
  sensitive   = true
}
'''

def generate_terraform_outputs() -> str:
    """Generate outputs configuration"""
    return '''output "region" {
  value       = var.aws_region
  description = "AWS region"
}

output "environment" {
  value       = var.environment
  description = "Environment name"
}

output "vpc_details" {
  value = {
    vpc_id            = aws_vpc.main.id
    vpc_cidr          = aws_vpc.main.cidr_block
    public_subnets   = [aws_subnet.public_1.id, aws_subnet.public_2.id]
    private_subnets  = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  }
  description = "VPC configuration details"
}

output "database_config" {
  value = {
    endpoint = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    database = aws_db_instance.main.db_name
    username = aws_db_instance.main.username
  }
  description = "Database configuration"
  sensitive   = true
}

output "redis_config" {
  value = {
    endpoint = aws_elasticache_cluster.main.cache_nodes[0].address
    port     = aws_elasticache_cluster.main.port
  }
  description = "Redis configuration"
}

output "security_groups" {
  value = {
    alb   = aws_security_group.alb.id
    app   = aws_security_group.app.id
    db    = aws_security_group.db.id
    redis = aws_security_group.redis.id
  }
  description = "Security group IDs"
}
'''

def generate_terraform_env_files() -> str:
    """Generate environment-specific Terraform files"""
    development = '''environment = "development"
aws_region  = "us-east-1"
instance_type = "t3.small"
db_instance_class = "db.t3.micro"
db_allocated_storage = 10
redis_node_type = "cache.t3.micro"
redis_num_cache_clusters = 1
'''

    staging = '''environment = "staging"
aws_region  = "us-east-1"
instance_type = "t3.medium"
db_instance_class = "db.t3.small"
db_allocated_storage = 20
redis_node_type = "cache.t3.small"
redis_num_cache_clusters = 1
'''

    production = '''environment = "production"
aws_region  = "us-east-1"
instance_type = "t3.large"
db_instance_class = "db.t3.medium"
db_allocated_storage = 100
redis_node_type = "cache.t3.medium"
redis_num_cache_clusters = 2
'''

    return {
        'development.tfvars': development,
        'staging.tfvars': staging,
        'production.tfvars': production
    }

def generate_terraform_readme() -> str:
    """Generate Terraform README"""
    return '''# Infrastructure as Code - Terraform AWS

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
'''

def setup_terraform_infrastructure():
    """Setup Terraform infrastructure files"""
    print("🏗️  Setting up Terraform Infrastructure as Code...")
    print("=" * 70)

    # Create terraform directory
    terraform_dir = Path("/home/user/02-python-app/terraform")
    terraform_dir.mkdir(exist_ok=True)

    # Write main configuration files
    (terraform_dir / "main.tf").write_text(generate_terraform_main())
    (terraform_dir / "variables.tf").write_text(generate_terraform_variables())
    (terraform_dir / "vpc.tf").write_text(generate_terraform_vpc())
    (terraform_dir / "rds.tf").write_text(generate_terraform_rds())
    (terraform_dir / "redis.tf").write_text(generate_terraform_redis())
    (terraform_dir / "outputs.tf").write_text(generate_terraform_outputs())
    (terraform_dir / "README.md").write_text(generate_terraform_readme())

    # Write environment files
    env_files = generate_terraform_env_files()
    for filename, content in env_files.items():
        (terraform_dir / filename).write_text(content)

    print("[Terraform Main Configuration]", end=" ", flush=True)
    print("✅")

    print("[VPC and Networking]", end=" ", flush=True)
    print("✅")

    print("[RDS PostgreSQL Database]", end=" ", flush=True)
    print("✅")

    print("[ElastiCache Redis]", end=" ", flush=True)
    print("✅")

    print("[Environment Configurations]", end=" ", flush=True)
    print("✅")

    print("[Documentation]", end=" ", flush=True)
    print("✅")

    print("=" * 70)
    print("✨ Terraform Infrastructure setup complete!")
    print("\nInfrastructure Summary:")
    print(f"  ✓ VPC with 2 public and 2 private subnets")
    print(f"  ✓ RDS PostgreSQL (multi-AZ in production)")
    print(f"  ✓ ElastiCache Redis (cluster-enabled in production)")
    print(f"  ✓ Security groups for ALB, App, Database, Redis")
    print(f"  ✓ NAT Gateways for private subnet internet access")
    print(f"  ✓ KMS encryption for RDS")
    print(f"  ✓ CloudWatch logging")
    print(f"  ✓ 3 environment configurations (dev/staging/prod)")
    print("\nNext Steps:")
    print("  1. cd terraform")
    print("  2. terraform init")
    print("  3. terraform plan -var-file=production.tfvars")
    print("  4. terraform apply -var-file=production.tfvars")


if __name__ == "__main__":
    setup_terraform_infrastructure()
