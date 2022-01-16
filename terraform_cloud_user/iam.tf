resource "aws_iam_user" "data_engineer" {
  name = "data_engineer"
}

resource "aws_iam_policy_attachment" "lakeformation" {
  name       = "lakeformation_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_policy_attachment" "s3" {
  name       = "s3_data_egineer"
  users      = [aws_iam_user.data_engineer.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

