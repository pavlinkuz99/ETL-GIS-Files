from loguru import logger
from osgeo import gdal

from etl_gis_files.config.config import gdal_settings


def vector_clip(input_path: str, output_path: str):
    try:
        gdal.Run(
            "vector",
            "clip",
            input=input_path,
            output=output_path,
            arguments=gdal_settings.algs.vector_clip,
        )
    except Exception as e:
        logger.error(f"Ошибка обработки {input_path}.\n{e} ")
    else:
        logger.info(f"Данные {input_path} обработаны. ")


def vector_convert(input_path: str, output_path: str):
    try:
        gdal.Run(
            "vector",
            "convert",
            input=input_path,
            output=output_path,
            arguments=gdal_settings.algs.vector_convert,
        )
    except Exception as e:
        logger.error(f"Ошибка обработки {input_path}.\n{e} ")
    else:
        logger.info(f"Данные {input_path} обработаны. ")


def vector_concat(input_path: str, output_path: str, output_layer: str):
    try:
        gdal.Run(
            "vector",
            "concat",
            input=input_path,
            output=output_path,
            output_layer=output_layer,
            arguments=gdal_settings.algs.vector_concat,
        )
    except Exception as e:
        logger.error(f"Ошибка обработки {input_path}.\n{e} ")
    else:
        logger.info(f"Данные {input_path} обработаны. ")
