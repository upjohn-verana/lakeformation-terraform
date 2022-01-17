resource "aws_iam_role" "glue_role" {
  name               = "glue-job-run-role"
  assume_role_policy = data.aws_iam_policy_document.s3.json
}

data "aws_iam_policy_document" "s3" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "logs" {
  statement {
    resources = ["*"]
    actions   = ["logs:*"]
  }
}

resource "aws_iam_policy" "logs" {
  name   = "logs_glue"
  policy = data.aws_iam_policy_document.logs.json
}

resource "aws_iam_policy_attachment" "logs_attach" {
  name       = "logs_attached"
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = aws_iam_policy.logs.arn
}

resource "aws_iam_user" "data_engineer" {
  name = "data_engineer"
}

resource "aws_iam_policy_attachment" "lakeformation-glue" {
  name       = "lakeformation_glue_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_policy_attachment" "lakeformation" {
  name       = "lakeformation_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSLakeFormationDataAdmin"
}

resource "aws_iam_policy_attachment" "s3" {
  name       = "s3_data_egineer"
  users      = [aws_iam_user.data_engineer.name]
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

data "aws_iam_policy_document" "lakeformation_basics" {
  statement {
    sid = "1"

    resources = [
      "*"
    ]
    actions = [
      "lakeformation:RegisterResource",
    ]

  }
}

resource "aws_iam_policy" "lakeformation_basics" {
  name   = "lakeformation_basics_policy"
  policy = data.aws_iam_policy_document.lakeformation_basics.json
}

resource "aws_iam_policy_attachment" "lakeformation_data_engineer" {
  name       = "lakeformation_basices_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  policy_arn = aws_iam_policy.lakeformation_basics.arn
}
