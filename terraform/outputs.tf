output "region" {
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
