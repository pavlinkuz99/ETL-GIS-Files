from pathlib import Path

from dynaconf import Dynaconf


def get_raw_settings(settings_files: list[Path]) -> Dynaconf:
    settings = Dynaconf(
        root_path=Path().absolute(),
        settings_files=settings_files,
        merge_enabled=True,
        environments=True,
        load_dotenv=True
    )

    return settings
