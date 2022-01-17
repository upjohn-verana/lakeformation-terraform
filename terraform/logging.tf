resource "aws_cloudwatch_log_group" "glue" {
  name = "/aws-glue/jobs/output"
}

resource "aws_cloudwatch_log_group" "glue_error" {
  name = "/aws-glue/jobs/error"
}
