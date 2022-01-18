import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import lit

# from awsglue.job import Job
bucket = "chad-upjohn-20220101-lakeformation"

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# job = Job(glueContext)


def define_source_path(bucket: str) -> str:
    path = f"s3://{bucket}/source_files/"
    return path


def define_destination_path(bucket: str) -> str:
    path = f"s3a://{bucket}/destination_files/"
    return path


def main():
    source = define_source_path(bucket)
    print(f"Defined source path: {dict(source_path=source)}")
    destination = define_destination_path(bucket)
    print(f"Defined destination path: {dict(destionation_path=destination)}")

    print("Start")
    df = spark.read.csv(
        source,
        sep=",",
        inferSchema=True,
        encoding="latin1",
        header=True,
        mode="PERMISSIVE",
    )

    df = df.withColumn("error_record", lit("what"))

    df.write.mode("overwrite").parquet(destination)


if __name__ == "__main__":
    # job.init(args["JOB_NAME"], args)

    print("Look at me")
    logger = glueContext.get_logger()
    logger.info("Hey there")

    main()
    # job.commit()
