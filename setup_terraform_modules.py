#!/usr/bin/env python3
"""
Terraform Modules Setup
Creates reusable Terraform modules for AWS resources
"""

from pathlib import Path

def generate_iam_module() -> dict:
    """Generate IAM module files"""
    main_tf = '''# IAM Role for Elastic Beanstalk EC2 instances
resource "aws_iam_role" "eb_ec2_role" {
  name = "${var.project_name}-eb-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policies
resource "aws_iam_role_policy_attachment" "eb_ec2_web_tier" {
  role       = aws_iam_role.eb_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
}

resource "aws_iam_role_policy_attachment" "eb_ec2_worker_tier" {
  role       = aws_iam_role.eb_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWorkerTier"
}

resource "aws_iam_role_policy_attachment" "eb_ec2_multicontainer_docker" {
  role       = aws_iam_role.eb_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkMulticontainerDocker"
}

# CloudWatch agent policy
resource "aws_iam_role_policy_attachment" "cloudwatch_agent" {
  role       = aws_iam_role.eb_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# ECR access for pulling images
resource "aws_iam_role_policy" "ecr_access" {
  name = "${var.project_name}-ecr-access"
  role = aws_iam_role.eb_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ]
        Resource = "*"
      }
    ]
  })
}

# RDS and Redis access
resource "aws_iam_role_policy" "db_access" {
  name = "${var.project_name}-db-access"
  role = aws_iam_role.eb_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds-db:connect"
        ]
        Resource = "arn:aws:rds-db:*:*:dbuser:*/*"
      }
    ]
  })
}

# Secrets Manager access
resource "aws_iam_role_policy" "secrets_manager_access" {
  name = "${var.project_name}-secrets-access"
  role = aws_iam_role.eb_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = "arn:aws:secretsmanager:*:*:secret:${var.project_name}/*"
      }
    ]
  })
}

# S3 access for static files
resource "aws_iam_role_policy" "s3_access" {
  name = "${var.project_name}-s3-access"
  role = aws_iam_role.eb_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      }
    ]
  })
}

# Instance profile
resource "aws_iam_instance_profile" "eb_ec2_profile" {
  name = "${var.project_name}-eb-ec2-profile"
  role = aws_iam_role.eb_ec2_role.name
}

# IAM role for Elastic Beanstalk service
resource "aws_iam_role" "eb_service_role" {
  name = "${var.project_name}-eb-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "elasticbeanstalk.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eb_service_policy" {
  role       = aws_iam_role.eb_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth"
}

output "eb_ec2_instance_profile" {
  value       = aws_iam_instance_profile.eb_ec2_profile.name
  description = "EB EC2 instance profile name"
}

output "eb_service_role_arn" {
  value       = aws_iam_role.eb_service_role.arn
  description = "EB service role ARN"
}

output "eb_ec2_role_arn" {
  value       = aws_iam_role.eb_ec2_role.arn
  description = "EB EC2 role ARN"
}
'''

    variables_tf = '''variable "project_name" {
  description = "Project name"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 bucket name for static files"
  type        = string
}
'''

    return {
        'main.tf': main_tf,
        'variables.tf': variables_tf
    }

def generate_elastic_beanstalk_module() -> dict:
    """Generate Elastic Beanstalk module files"""
    main_tf = '''# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_app" "main" {
  name            = "${var.project_name}-app"
  description     = "Elastic Beanstalk application"
  appversion_lifecycle {
    service_role          = var.service_role_arn
    max_age_in_days       = 30
    delete_source_from_s3 = true
  }
}

# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "main" {
  name                = "${var.project_name}-env"
  application         = aws_elastic_beanstalk_app.main.name
  solution_stack_name = "64bit Amazon Linux 2 v5.8.5 running Python 3.11"
  tier                = "WebServer"
  instance_type       = var.instance_type

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = var.min_instances
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = var.max_instances
  }

  setting {
    namespace = "aws:ec2:instances"
    name      = "InstanceTypes"
    value     = var.instance_type
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = var.vpc_id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", var.private_subnet_ids)
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = join(",", var.public_subnet_ids)
  }

  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "StreamLogs"
    value     = "true"
  }

  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "DeleteOnTerminate"
    value     = "false"
  }

  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "RetentionInDays"
    value     = "7"
  }

  # Environment variables
  dynamic "setting" {
    for_each = var.environment_variables
    content {
      namespace = "aws:elasticbeanstalk:application:environment"
      name      = setting.key
      value     = setting.value
    }
  }

  depends_on = [
    aws_elastic_beanstalk_app.main
  ]
}

output "environment_name" {
  value       = aws_elastic_beanstalk_environment.main.name
  description = "Elastic Beanstalk environment name"
}

output "environment_endpoint" {
  value       = aws_elastic_beanstalk_environment.main.endpoint_url
  description = "Elastic Beanstalk environment endpoint"
}

output "cname" {
  value       = aws_elastic_beanstalk_environment.main.cname
  description = "Elastic Beanstalk CNAME"
}
'''

    variables_tf = '''variable "project_name" {
  description = "Project name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 2
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 4
}

variable "service_role_arn" {
  description = "Service role ARN"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables"
  type        = map(string)
  default     = {}
}
'''

    return {
        'main.tf': main_tf,
        'variables.tf': variables_tf
    }

def generate_alb_module() -> dict:
    """Generate Application Load Balancer module"""
    main_tf = '''# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.enable_deletion_protection
  enable_http2               = true
  enable_cross_zone_load_balancing = true

  tags = {
    Name = "${var.project_name}-alb"
  }
}

# Target Group
resource "aws_lb_target_group" "main" {
  name        = "${var.project_name}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  tags = {
    Name = "${var.project_name}-tg"
  }
}

# HTTP Listener (redirect to HTTPS)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# HTTPS Listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "ALB DNS name"
}

output "target_group_arn" {
  value       = aws_lb_target_group.main.arn
  description = "Target group ARN"
}

output "alb_arn" {
  value       = aws_lb.main.arn
  description = "ALB ARN"
}
'''

    variables_tf = '''variable "project_name" {
  description = "Project name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "ALB security group ID"
  type        = string
}

variable "certificate_arn" {
  description = "SSL certificate ARN"
  type        = string
}

variable "enable_deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = false
}
'''

    return {
        'main.tf': main_tf,
        'variables.tf': variables_tf
    }

def setup_terraform_modules():
    """Setup Terraform modules"""
    print("📦 Setting up Terraform Modules...")
    print("=" * 70)

    modules_dir = Path("/home/user/02-python-app/terraform/modules")
    modules_dir.mkdir(exist_ok=True)

    # IAM Module
    iam_dir = modules_dir / "iam"
    iam_dir.mkdir(exist_ok=True)
    iam_files = generate_iam_module()
    for filename, content in iam_files.items():
        (iam_dir / filename).write_text(content)
    print("[IAM Module]", end=" ", flush=True)
    print("✅")

    # Elastic Beanstalk Module
    eb_dir = modules_dir / "elastic_beanstalk"
    eb_dir.mkdir(exist_ok=True)
    eb_files = generate_elastic_beanstalk_module()
    for filename, content in eb_files.items():
        (eb_dir / filename).write_text(content)
    print("[Elastic Beanstalk Module]", end=" ", flush=True)
    print("✅")

    # ALB Module
    alb_dir = modules_dir / "alb"
    alb_dir.mkdir(exist_ok=True)
    alb_files = generate_alb_module()
    for filename, content in alb_files.items():
        (alb_dir / filename).write_text(content)
    print("[ALB Module]", end=" ", flush=True)
    print("✅")

    print("=" * 70)
    print("✨ Terraform modules setup complete!")
    print("\nAvailable Modules:")
    print("  ✓ modules/iam - IAM roles and policies")
    print("  ✓ modules/elastic_beanstalk - EB application")
    print("  ✓ modules/alb - Application Load Balancer")


if __name__ == "__main__":
    setup_terraform_modules()
