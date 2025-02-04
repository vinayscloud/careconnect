# outputs.tf

output "vpc_id" {
  value = aws_vpc.my_vpc.id
}

output "subnet_id" {
  value = aws_subnet.my_subnet.id
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.my_ecs_cluster.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.my_ecr_repository.repository_url
}
