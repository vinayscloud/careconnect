resource "aws_iam_user" "user" {
  name = "terraform_user" 
}

resource "aws_iam_user_login_profile" "example_login_profile" {
  user    = aws_iam_user.user.name
  password_reset_required = true
}


resource "aws_iam_policy" "policy" {
  name        = "test_policy"
  path        = "/"
  description = "My test policy"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "*",
        ]
        Effect   = "Allow"
        Resource = [var.resource]
      },
    ]
  })
}


resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  users      = [aws_iam_user.user.name]
  policy_arn = aws_iam_policy.policy.arn
}