default:
    @just --list

terraform_init:
    cd ./terraform && \
    AWS_PROFILE=cloud_guru terraform init

terraform_plan:
    cd ./terraform && \
    AWS_PROFILE=cloud_guru terraform plan

terraform_apply:
    cd ./terraform && \
    AWS_PROFILE=cloud_guru terraform apply -auto-approve

terraform_clean:
    rm ./terraform/terraform.tfstate*

copy_one_csv:
    aws s3 cp one.csv s3://chad-upjohn-20220101-lakeformation/

run_glue:
    AWS_PROFILE=cloud_guru poetry run python src/run_glue_job.py
