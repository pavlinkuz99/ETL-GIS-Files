from zoneinfo import ZoneInfo

from pydantic import BaseModel, confloat

from etl_gis_files.config.models.db import DBSettings
from etl_gis_files.config.models.dirs_files import DirsFilesSettings


class Settings(BaseModel):
    tz: ZoneInfo
    cpu_cores_frac: confloat(gt=0, lt=1)
    db_exec_base_command: str
    db_dump_base_command: str
    db_restore_base_command: str
    dirs_files: DirsFilesSettings
    db: DBSettings
