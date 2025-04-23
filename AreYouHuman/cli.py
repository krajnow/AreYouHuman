import zipfile
import os

import alive_progress
import requests
import click


GITHUB_ZIP = "https://github.com/krajnow/AreYouHuman/raw/refs/heads/master/emojis.zip"


@click.group()
def cli() -> None:
    """Command Line Interface."""


@cli.command()
@click.option("--output-zip", default="emojis.zip")
def download(output_zip: str) -> None:
    """
    Downloading the archive with all the emojis for rendering.
    Also unpacking it into the current directory.
    """
    try:
        with requests.get(url=GITHUB_ZIP, stream=True) as response:
            response.raise_for_status()

            length = int(response.headers.get("content-length", 0))

            with alive_progress.alive_bar(
                title=output_zip,
                total=length,
                bar="smooth",
            ) as bar, open(output_zip, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        bar(len(chunk))

        with zipfile.ZipFile(output_zip) as zip_file:
            zip_file.extractall()

        os.remove(output_zip)

        click.echo("✅ All downloads completed!")

    except requests.exceptions.HTTPError as error:
        click.echo(f"❌ HTTPError: {error}", err=True)
    except Exception as error:
        click.echo(f"❌ Error: {error}", err=True)
