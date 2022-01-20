from loguru import logger


def define_source_path(bucket: str) -> str:
    logger.info("Setting source path")
    path = f"s3://{bucket}/source_files/"
    return path
