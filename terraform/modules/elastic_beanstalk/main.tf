# Elastic Beanstalk Application
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
