variable "counter" {
  type     = number
}
variable "create_ec2_instance" {
  type = bool
  
}
variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
}

variable "public_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_cidrs" {
  description = "List of CIDR blocks for private subnets"
  type        = list(string)
}

variable "azs" {
  description = "List of availability zones"
  type        = list(string)
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}
