#s3 bucket

module "s3_bucket" {
  source = "./modules/s3"
}

#SG

module "vpc" {
  source = "./modules/vpc"  
  environment=var.environment
  azs = var.azs
  public_cidrs= var.public_cidrs
  private_cidrs = var.private_cidrs
  vpc_cidr = var.vpc_cidr
}

