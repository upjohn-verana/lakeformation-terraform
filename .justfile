default:
    @just --list

bucket := "chad-upjohn-20220101-lakeformation"

terraform_fresh_start: terraform_clean terraform_apply copy_one_csv zip_utils

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
    aws s3 cp local_scripts/one.csv s3://{{bucket}}/

zip_utils:
    cd ./src && zip -r glue_utils.zip glue_utils/* && cd -
    aws s3 cp ./src/glue_utils.zip s3://{{bucket}}/glue_script/glue_utils/glue_utils.zip
    cd ./src && rm -r glue_utils.zip && cd -

run_glue:
    AWS_PROFILE=cloud_guru poetry run python local_scripts/run_glue_job.py
