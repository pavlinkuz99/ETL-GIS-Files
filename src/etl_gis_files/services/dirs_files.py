from pathlib import Path


def get_paths_and_names(
    schemas_path: Path,
    schemas_converted_path: Path,
    unary_format_for_converted_layers: str,
    file_layers_name_patterns: list[str],
) -> tuple[set[str], list[tuple], set[Path], list[tuple]]:

    schemas_names = set()
    tables_paths_and_names = set()
    for path in schemas_path.glob("*/*/"):
        if path.is_dir():
            schemas_names.add(path.parent.stem)
            tables_paths_and_names.add(
                (
                    schemas_converted_path / path.relative_to(schemas_path),
                    f"{path.parent.stem}.{path.stem}",
                )
            )

    file_layers_converted_dir_paths = set()
    file_layers_paths = set()
    for file_layers_suffix in file_layers_name_patterns:
        for file_layer_path in schemas_path.rglob(f"{file_layers_suffix}"):
            file_layer_converted_path = (
                schemas_converted_path
                / file_layer_path.relative_to(schemas_path).with_suffix(
                    unary_format_for_converted_layers
                )
            )
            file_layers_converted_dir_paths.add(file_layer_converted_path.parent)
            file_layers_paths.add((file_layer_path, file_layer_converted_path))

    return (
        schemas_names,
        list(zip(*tables_paths_and_names)),
        file_layers_converted_dir_paths,
        list(zip(*file_layers_paths)),
    )


def mkdirs(paths: set[Path]):
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
