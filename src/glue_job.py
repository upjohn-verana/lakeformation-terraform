import sys

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from glue_utils.glue_util import define_source_path
from loguru import logger
from pyspark.context import SparkContext
from pyspark.sql.functions import lit

# from awsglue.job import Job
bucket = "chad-upjohn-20220101-lakeformation"

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
# job = Job(glueContext)


def define_destination_path(bucket: str) -> str:
    path = f"s3a://{bucket}/destination_files/"
    return path


def main():
    source = define_source_path(bucket)
    logger.info(f"Defined source path: {dict(source_path=source)}")
    destination = define_destination_path(bucket)
    logger.info(f"Defined destination path: {dict(destionation_path=destination)}")

    logger.info("Start")
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

    logger.warning("Look at me")
    glue_logger = glueContext.get_logger()
    glue_logger.info("A gluelogger: Hey there")

    log4jLogger = spark._jvm.org.apache.log4j
    log_4j = log4jLogger.LogManager.getLogger(__name__)
    log_4j.warn("Log4j: Hello World!")

    logger.info("Loguru forever")
    logger.debug("Adding loguru")

    main()
    # job.commit()
