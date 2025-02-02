counter = 1
create_ec2_instance= true
vpc_cidr    = "10.0.0.0/16"
public_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
azs         = ["us-east-1a", "us-east-1b"]
environment = "dev"
