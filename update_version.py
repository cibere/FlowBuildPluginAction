# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///

from pathlib import Path
import click
import json


@click.command
@click.argument("suffix")
def main(suffix: str):
    file = Path("plugin.json")
    data = json.loads(file.read_text())
    data["Version"] = f"{data['Version']}-{suffix}"
    file.write_text(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
