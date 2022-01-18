import time

import boto3

account_number = "830978417405"
bucket = "chad-upjohn-20220101-lakeformation"
glue_job_name = "cloud_guru_glue_job"

script_location = f"s3://{bucket}/glue_script/glue_job.py"


def get_glue_client():
    return boto3.client("glue", "us-east-1")


def get_glue_jobs():
    glue = get_glue_client()
    paginator = glue.get_paginator("get_jobs")

    glue_jobs = []
    pages = paginator.paginate()
    for page in pages:
        for job in page["Jobs"]:
            glue_jobs.append(job["Name"])
    return glue_jobs


def create_glue_job():
    glue = get_glue_client()
    glue.create_job(
        Name=glue_job_name,
        Role=f"arn:aws:iam::{account_number}:role/glue-job-run-role",
        Command={
            "Name": "glueetl",
            "ScriptLocation": script_location,
            "PythonVersion": "3",
        },
        DefaultArguments={
            "--TempDir": f"s3://{bucket}/glue_script/temp/",
            "--enable-continuous-cloudwatch-log": "true",
            "--enable-continuous-log-filter": "false",
            "--enable-metrics": "",
            "--job-bookmark-option": "job-bookmark-disable",
            "--job-language": "python",
        },
        MaxRetries=0,
        Timeout=2880,
        GlueVersion="2.0",
        WorkerType="Standard",
        NumberOfWorkers=1,
    )


def run_glue_job():
    glue = get_glue_client()
    result = glue.start_job_run(JobName=glue_job_name)

    status = glue.get_job_run(JobName=glue_job_name, RunId=result["JobRunId"])
    while status["JobRun"]["JobRunState"] == "RUNNING":
        print("still running")
        time.sleep(10)
        status = glue.get_job_run(JobName=glue_job_name, RunId=result["JobRunId"])

    print(f"Job: {status['JobRun']['JobRunState']}")

    print("Done")
