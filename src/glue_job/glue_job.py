import json
import re
from pathlib import Path
from typing import List

import s3fs
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, input_file_name, lit
from pyspark.sql.types import StructType

fs = s3fs.S3FileSystem()

spark = SparkSession.builder.getOrCreate()
log4j = spark._jvm.org.apache.log4j
log4j.LogManager.getRootLogger().setLevel(log4j.Level.ERROR)

destination_preprocessed_file = "vh-master-ue1-dev-data-lake"

destination_bucket = "vh-master-ue1-dev-data-lake"
base_prefix = "raw/epic"
processing_config_prefix = "processing_config"
raw_landing_csv_prefix = "{ingestion_id}/raw_landing_csv"
pre_processed_location_prefix = "{ingestion_id}/pre-processed"

preprocess_path = f"s3://{destination_bucket}/{base_prefix}/{pre_processed_location_prefix}"
raw_landing_path = f"s3://{destination_bucket}/{base_prefix}/{raw_landing_csv_prefix}/"

config_file_name = "config.json"
config_s3_path = f"s3://{destination_bucket}/{base_prefix}/{processing_config_prefix}/{config_file_name}"


def pull_list_of_files_to_preprocess(ingestion_id: str) -> List:
    raw_landing_with_ingestion_id_path = raw_landing_path.format(ingestion_id=ingestion_id)

    list_of_raw_files = fs.ls(raw_landing_with_ingestion_id_path)
    return list_of_raw_files


def pull_table_name(path_stem: str) -> str:
    regex_ = r"(.*?)([-_]?\d{4}[_-]?\d{2}[_-]?\d{2})"
    matching = re.search(regex_, path_stem)
    groupings = matching.groups()
    table_name = groupings[0].lower()
    return table_name


def retrieve_table_name_from_file_name(s3_file_path: str) -> str:
    path_object = Path(s3_file_path)
    table_name = pull_table_name(path_object.stem)
    return table_name


def main(ingestion_id: str, record_separator: str) -> None:
    preprocess_with_ingestion_id_path = preprocess_path.format(ingestion_id=ingestion_id)

    files_to_preprocess = pull_list_of_files_to_preprocess(ingestion_id)
    table_name_with_s3_path = [
        (retrieve_table_name_from_file_name(file_path), f"s3://{file_path}") for file_path in files_to_preprocess
    ]
    print(f"Files: {dict(table_with_file_name=table_name_with_s3_path)}")
    for table_name, s3_path in table_name_with_s3_path:
        print(s3_path)

        df = spark.read.csv(
            s3_path,
            sep=record_separator,
            inferSchema=True,
            encoding="latin1",
            header=True,
            mode="PERMISSIVE",
        )

        df = df.withColumn("error_record", lit(""))

        print(f"datatyes are {dict(types=df.dtypes)}")

        for column_ in df.dtypes:
            column_name = column_[0]
            if " " in column_name:
                print(f"looping through columns: {dict(column=column_name)}")
                df = df.withColumnRenamed(column_name, column_name.replace(" ", "_").replace("(", "").replace(")", ""))

        columns_ = df.schema.jsonValue()
        print(f"Columns retrieved {dict(columns=columns_)}")

        df_schema = StructType.fromJson(columns_)

        df_inferred_schema = spark.read.csv(
            s3_path,
            sep=record_separator,
            schema=df_schema,
            inferSchema=False,
            encoding="latin1",
            header=True,
            columnNameOfCorruptRecord="error_record",
            mode="PERMISSIVE",
        )

        df = df_inferred_schema.withColumn("source_file_name", input_file_name())

        # get good records
        good_df = df_inferred_schema.filter(col("error_record").isNull())

        # drop error column
        good_df = good_df.drop("error_record")

        save_s3_table_name = f"{preprocess_with_ingestion_id_path}/{table_name}".replace("s3://", "s3a://")
        print(save_s3_table_name)
        good_df.write.mode("overwrite").parquet(save_s3_table_name)


if __name__ == "__main__":
    with fs.open(config_s3_path) as f:
        config = json.load(f)
    ingestion_id = config["ingestion_id"]
    record_separator = config["record_separator"]
    main(ingestion_id, record_separator)
