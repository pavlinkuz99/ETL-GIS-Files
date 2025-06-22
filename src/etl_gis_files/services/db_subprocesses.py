import subprocess
from datetime import datetime

from loguru import logger

from etl_gis_files.config.config import settings


def init_db(db_dsn: str, schemas_names: set[str]):
    for schema_name in schemas_names:
        stmt = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        exec_command = f"""{settings.db_exec_base_command} -d "{db_dsn}" -c "{stmt}" """
        try:
            subprocess.run(exec_command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"{stmt}: {e}")
        else:
            logger.info(schema_name)


def dump_db(schemas_names: set[str], thread_pool_size: int, db_dsn: str):
    logger.info("Создание дампов схем ... ")
    current_timestamp = datetime.now(settings.tz)
    formatted_timestamp = current_timestamp.strftime("%Y%m%d_%H%M%S")
    for schema_name in schemas_names:
        file_path = (
            settings.dirs_files.output_path / f"{schema_name}_{formatted_timestamp}"
        )
        dump_command = f"""{settings.db_dump_base_command} -j {thread_pool_size} -d "{db_dsn}" -n {schema_name} -f {file_path}"""
        try:
            subprocess.run(dump_command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка создания дампа {file_path}: {e}")
        else:
            logger.info(f"Дамп {file_path} создан.")


def restore_db(thread_pool_size: int, db_dsn: str):
    logger.info("Восстановление схем из дампов... ")
    for path in settings.dirs_files.output_path.glob("*"):
        if path.is_dir():
            restore_command = f"""{settings.db_restore_base_command} -j {thread_pool_size} -d "{db_dsn}" {path}"""
            try:
                subprocess.run(restore_command, check=True, shell=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Ошибка восстановления из дампа {path}: {e}")
            else:
                logger.info(f"Дамп {path} восстановлен.")
