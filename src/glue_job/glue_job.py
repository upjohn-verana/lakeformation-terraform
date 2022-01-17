import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

"""
Need to create a db and table for running this

db: chad-db
table: source_files
"""

# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

bucket = "chad-upjohn-20220101-lakeformation"

db = "chad-db"
table = "source_files"
print(f"Start dynamic thing: {dict(db=db, table=table)}")

tx_id = glueContext.start_transaction(False)

datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database=db, table_name=table, transformation_ctx="datasource0"
)
print(datasource0.show())

dest_path = f"s3://{bucket}/new_destination/"

sink = glueContext.getSink(connection_type="s3", path=dest_path, enableUpdateCatalog=True, transactionId=tx_id)
sink.setFormat("glueparquet")
sink.setCatalogInfo(catalogDatabase="retail", catalogTableName="destionation_table")

try:
    sink.writeFrame(datasource0)
    glueContext.commit_transaction(tx_id)
except Exception:
    glueContext.cancel_transaction(tx_id)
    raise
job.commit()
