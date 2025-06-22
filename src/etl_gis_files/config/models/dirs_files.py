from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class DirsFilesSettings(BaseModel):
    schemas_path: Path
    schemas_converted_path: Path
    unary_format_for_converted_layers: Literal[".parquet", ".gpkg.zip"]
    file_layers_name_patterns: set[str]
    output_path: Path
