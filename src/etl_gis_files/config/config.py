import sys
from pathlib import Path

from loguru import logger

from etl_gis_files.config.models.common import Settings
from etl_gis_files.config.loader import get_raw_settings

settings_files = []
default_settings_files_template = Path(__file__).parent.absolute() / "*.toml"
settings_files.append(default_settings_files_template)

settings = get_raw_settings(settings_files)

gdal_settings = settings.GDAL_SETTINGS
settings = Settings(**settings.SETTINGS.to_dict())


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    logger.debug(gdal_settings)
    logger.debug(settings.model_dump_json(indent=2))
