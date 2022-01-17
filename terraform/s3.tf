variable "bucket_name_addition" {
  type    = string
  default = "20220101"
}

# resource "aws_s3_bucket" "source" {
#   bucket = "chad-upjohn-${var.bucket_name_addition}-source"
# }

resource "aws_s3_bucket" "lakeformation" {
  bucket = "chad-upjohn-${var.bucket_name_addition}-lakeformation"
}

