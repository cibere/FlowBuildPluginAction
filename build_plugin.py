# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///

import zipfile
import click
import re
from pathlib import Path
from click.types import StringParamType
from typing import Any


class ZipFileParamType(StringParamType):
    def convert(
        self, value: Any, param: click.Parameter | None, ctx: click.Context | None
    ):
        converted: str = super().convert(value, param, ctx)
        if not converted.endswith(".zip"):
            raise ValueError("Archive Name must end with .zip")
        return converted


@click.command
@click.argument("archive_name", type=ZipFileParamType())
@click.option("--included-directories")
@click.option("--included-files")
@click.option("-re", "--regex")
@click.option("-ex", "--exclude-defaults")
@click.option("-lib", "--lib-directory", default="lib")
@click.option("--ignored-extensions", default=".dist-info,.pyc,__pycache__,.pyi")
def main(
    archive_name: str,
    included_directories: str | None,
    included_files: str | None,
    regex: str | None,
    exclude_defaults: str,
    lib_directory: str,
    ignored_extensions: str
):
    root = Path("")
    ignore_exts = tuple(ignored_extensions.split(","))

    files_to_add = []

    if included_files:
        files_to_add.extend([Path(fp.strip()) for fp in included_files.split(",")])
    if included_directories:
        files_to_add.extend(
            [
                file
                for fp in included_directories.split(",")
                for file in Path(fp.strip()).rglob("*")
                if not file.name.endswith(ignore_exts)
            ]
        )
    if not exclude_defaults:
        files_to_add.extend(
            path
            for fp in ["SettingsTemplate.yaml", "plugin.json"]
            if (path := Path(fp)).exists()
        )

    files_to_add.extend(
        [
            file
            for file in Path(lib_directory).rglob("*")
            if not file.parent.parent.name.endswith(
                ignore_exts  # some deps include a licenses dir inside of their dist-info dir
            )
            and not file.parent.name.endswith(ignore_exts)
            and not file.name.endswith(ignore_exts)
        ]
    )

    if regex:
        pattern = re.compile(regex)
        files_to_add.extend(
            [
                file
                for file in root.rglob("*")
                if pattern.search(str(file.relative_to(root)))
            ]
        )

    with zipfile.ZipFile(archive_name, "w") as f:
        for file in set(files_to_add):
            f.write(str(file))
            click.echo(f"Added {file}")

    click.echo(f"\nDone. Archive saved to {archive_name}")


if __name__ == "__main__":
    main()
