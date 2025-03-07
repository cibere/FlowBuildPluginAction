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
@click.option("--suffix")
@click.option("--final", is_flag=True)
def main(suffix: str | None, final: bool):
    file = Path("plugin.json")
    data = json.loads(file.read_text())
    current: str = data["Version"]

    if suffix:
        data["Version"] = f"{current}-{suffix}"
    elif final:
        for char in ("a", "b", "c"):
            if char in current:
                data['Version'] = current = current.split(char)[0]

    file.write_text(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
