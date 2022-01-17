import logging
from pathlib import Path

import boto3
from utils_run_glue_job import create_glue_job, get_glue_jobs, glue_job_name, run_glue_job, script_location

logging.basicConfig(format="%(asctime)s: %(module)s: %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    s3_client = boto3.client("s3")
    script_location_parts = Path(script_location).parts
    bucket = script_location_parts[1]
    s3_client.upload_file("./src/glue_job/glue_job.py", bucket, "/".join(script_location_parts[2:]))
    s3_client.upload_file("./src/one.csv", bucket, "one.csv")

    glue_jobs = get_glue_jobs()
    if glue_job_name not in glue_jobs:
        _ = create_glue_job()
    _ = run_glue_job()
