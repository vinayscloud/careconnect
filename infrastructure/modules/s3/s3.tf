resource "aws_s3_bucket" "my_bucket" {
  bucket = "careconnect-healthcare-clod" 

  tags = {
    Name        = "My Terraform Bucket"
    Environment = "Dev"
  }
}
