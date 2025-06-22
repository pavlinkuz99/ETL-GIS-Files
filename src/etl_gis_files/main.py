import os
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from osgeo import gdal

from etl_gis_files.config.config import settings
from etl_gis_files.config.config import gdal_settings
from etl_gis_files.services import gdal_algs
from etl_gis_files.services.dirs_files import get_paths_and_names, mkdirs
from etl_gis_files.services.db_subprocesses import init_db, dump_db


def process_etl(max_workers: int, db_dsn: str):
    schemas_names, tables_paths_and_names, file_layers_converted_dir_paths, file_layers_paths = (
        get_paths_and_names(
            settings.dirs_files.schemas_path,
            settings.dirs_files.schemas_converted_path,
            settings.dirs_files.unary_format_for_converted_layers,
            settings.dirs_files.file_layers_name_patterns,
        )
    )

    boundaries_path = gdal_settings.algs.vector_clip.get("like")
    format_reduce_func = (
        gdal_algs.vector_clip if boundaries_path else gdal_algs.vector_convert
    )

    logger.info("Сведение к единому формату (в целевых границах) ... ")
    mkdirs(file_layers_converted_dir_paths)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            format_reduce_func,
            file_layers_paths[0],
            file_layers_paths[1]
        )

    logger.info("Запись в базу данных ... ")
    init_db(db_dsn, schemas_names)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        output_path = len(tables_paths_and_names[0]) * [db_dsn]
        executor.map(
            gdal_algs.vector_concat,
            tables_paths_and_names[0],
            output_path,
            tables_paths_and_names[1],
        )

    dump_db(schemas_names, max_workers, db_dsn)


def main():
    logger.info("ETL-процесс GIS Files запущен. ")

    gdal.UseExceptions()
    logger.info(f"Версия GDAL: {gdal.__version__}. ")

    db_dsn = settings.db.dsn.unicode_string()
    cpu_cnt = os.cpu_count() or 1
    thread_pool_size = int(settings.cpu_cores_frac * cpu_cnt) + 1
    logger.info(f"Будет использовано потоков: {thread_pool_size}. ")

    process_etl(thread_pool_size, db_dsn)

    logger.info("ETL-процесс GIS Files завершен. ")


if __name__ == "__main__":
    main()
