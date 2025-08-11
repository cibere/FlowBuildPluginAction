# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
# ]
# ///

from pathlib import Path
import click
import os
import json

github_output = Path(os.environ["GITHUB_OUTPUT"])


@click.command
@click.option("--final", is_flag=True)
def main(final: bool):
    file = Path("plugin.json")
    data = json.loads(file.read_text())
    version: str = data["Version"]

    if final:
        for char in ("a", "b", "c"):
            if char in version:
                version = version.split(char)[0]

    data["Version"] = version
    file.write_text(json.dumps(data, indent=4))

    with github_output.open("a") as file:
        print(f"PLUGIN_VERSION={version}", file=file)


if __name__ == "__main__":
    main()
