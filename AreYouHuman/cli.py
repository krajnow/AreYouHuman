import os
from pathlib import Path
from typing import List
from urllib.parse import quote

import requests
import click
from alive_progress import alive_bar

from AreYouHuman.types import DefaultEmojis


EMOJIS_CDN: str = "https://emojicdn.elk.sh/%s?style=apple"
EMOJIS: List[str] = DefaultEmojis.emojis
OUTPUT: str = "emojis"


@click.group()
def cli() -> None:
    """Command Line Interface"""
    pass


@cli.command()
def download() -> None:
    """Downloading all emojis for rendering."""

    Path(OUTPUT).mkdir(exist_ok=True)

    files: List[str] = os.listdir(OUTPUT)
    emojis: List[str] = [quote(emoji) for emoji in EMOJIS if quote(emoji) not in files]
    length: int = len(emojis)

    with alive_bar(
        length,
        title="Downloading %s emojis." % length,
        spinner="dots_waves2"
    ) as bar:
        for emoji in emojis:
            url: str = EMOJIS_CDN % emoji
            save_path: Path = Path(OUTPUT) / emoji

            try:
                download_file(url, save_path)
                bar.text("D: %s" % emoji)
            except Exception as e:
                bar.text("E: %s (%s)" % (emoji, e))
            finally:
                bar()

    click.echo("All downloads completed!")


def download_file(
    url: str,
    save_path: Path
) -> None:
    """Download one emoji with a status bar."""
    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, 'wb') as f:
        f.write(response.content)
