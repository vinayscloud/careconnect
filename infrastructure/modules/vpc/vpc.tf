# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count             = length(var.public_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_cidrs[count.index]
  availability_zone = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.environment}-public-subnet-${count.index}"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count             = length(var.private_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_cidrs[count.index]
  availability_zone = var.azs[count.index]

  tags = {
    Name = "${var.environment}-private-subnet-${count.index}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.environment}-internet-gateway"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.environment}-nat-gateway"
  }
}

# Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.environment}-public-route-table"
  }
}

# Associate Route Table with Public Subnets
resource "aws_route_table_association" "public" {
  count          = length(var.public_cidrs)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "${var.environment}-private-route-table"
  }
}

# Associate Route Table with Private Subnets
resource "aws_route_table_association" "private" {
  count          = length(var.private_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
