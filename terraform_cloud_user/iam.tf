resource "aws_iam_user" "data_engineer" {
  name = "data_engineer"
}

resource "aws_iam_policy_attachment" "lakeformation-glue" {
  name       = "lakeformation_glue_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_policy_attachment" "lakeformation" {
  name       = "lakeformation_data_engineer"
  users      = [aws_iam_user.data_engineer.name]
  policy_arn = "arn:aws:iam::aws:policy/AWSLakeFormationDataAdmin"
}

resource "aws_iam_policy_attachment" "s3" {
  name       = "s3_data_egineer"
  users      = [aws_iam_user.data_engineer.name]
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
