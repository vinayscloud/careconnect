# variables.tf

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  default     = "10.0.1.0/24"
}

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "my-ecs-cluster"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  default     = "my-ecr-repository"
}
