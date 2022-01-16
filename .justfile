terraform_init_cloud_user:
    cd ./terraform_cloud_user && \
    AWS_PROFILE=cloud_guru terraform init

terraform_plan_cloud_user:
    cd ./terraform_cloud_user && \
    AWS_PROFILE=cloud_guru terraform plan

terraform_apply_cloud_user:
    cd ./terraform_cloud_user && \
    AWS_PROFILE=cloud_guru terraform apply -auto-approve

terraform_init_data_engineer:
    cd ./terraform_data_engineer && \
    AWS_PROFILE=data_engineer terraform init

terraform_plan_data_engineer:
    cd ./terraform_data_engineer && \
    AWS_PROFILE=data_engineer terraform plan

terraform_apply_data_engineer:
    cd ./terraform_data_engineer && \
    AWS_PROFILE=data_engineer terraform apply -auto-approve

copy_one_csv:
    aws s3 cp one.csv s3://chad-upjohn-20220101-lakeformation/

