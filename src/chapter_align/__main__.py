from pathlib import Path
import logging

import click
import colorama  # type: ignore
import pycountry  # type: ignore

from . import __version__
from .utils.misc import get_package_folders  # type: ignore
from .utils.misc import setup_logger
from .align import align_book
from .build_epub import build_epub


@click.command()
# book base folder
@click.option(
    "--book_base_folder",
    type=str,
    default=get_package_folders() / "data" / "leroux" / "yellow_room",
    help="The path to the book folder, that should contain the two language folders.",
    show_default=True,
)
# languages
@click.option(
    "--language0",
    type=str,
    default="english",
    help="The language tag (the subfolder) for l0.",
    show_default=True,
)
@click.option(
    "--language1",
    type=str,
    default="french",
    help="The language tag (the subfolder) for l1.",
    show_default=True,
)
# chapter template
@click.option(
    "--ch_template0",
    type=str,
    default="ch_{:04d}.xhtml",
    help="The chapters' template for l0.",
    show_default=True,
)
@click.option(
    "--ch_template1",
    type=str,
    default="main{}.xml",
    help="The chapters' template for l1.",
    show_default=True,
)
# chapter start index
@click.option(
    "--ch_start_index0",
    type=int,
    default=1,
    help="The first chapter index for l0.",
    show_default=True,
)
@click.option(
    "--ch_start_index1",
    type=int,
    default=0,
    help="The first chapter index for l1.",
    show_default=True,
)
# tot number of chapters
@click.option(
    "--tot_chapter_num",
    type=int,
    default=29,
    help="The number of chapters.",
    show_default=True,
)
# book author
@click.option(
    "--author_name",
    type=str,
    default="Gaston Leroux",
    help="The author of the book.",
    show_default=True,
)
# book author
@click.option(
    "--book_title",
    type=str,
    default="Le Mystère de la chambre jaune - Composed",
    help="The title of the book.",
    show_default=True,
)
# log options
@click.option(
    "--log_level_debug",
    type=click.Choice(
        ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="WARN",
    help="Level for the debugging logger.",
    show_default=True,
)
@click.option(
    "--log_level_type",
    type=click.Choice(["anlm", "nlm", "lm", "nm", "m"], case_sensitive=False),
    default="m",
    help="Message format for the debugging logger.",
    show_default=True,
)
@click.version_option(version=__version__)
def main(
    book_base_folder: str,
    ch_template0: str,
    ch_template1: str,
    ch_start_index0: int,
    ch_start_index1: int,
    language0: str,
    language1: str,
    tot_chapter_num: int,
    author_name: str,
    book_title: str,
    log_level_debug: str,
    log_level_type: str,
) -> None:
    r"""Align two sets of chapters in different languages."""
    setup_logger(log_level_debug, log_level_type)
    logg = logging.getLogger(f"c.{__name__}.main")
    logg.debug("Starting main")

    colorama.init()

    book_folder = Path(book_base_folder).expanduser().absolute()
    author_name_full = author_name
    book_name_full = book_title
    languages = language0, language1

    chapter_templates = ch_template0, ch_template1
    chapter_start_indexes = ch_start_index0, ch_start_index1

    align_book(
        book_folder,
        languages,
        chapter_templates,
        chapter_start_indexes,
        tot_chapter_num,
        author_name_full,
        book_name_full,
    )

    lang1 = pycountry.languages.get(name=languages[1])
    logg.debug(f"lang1: {lang1}")
    lang_alpha2_tag1 = lang1.alpha_2

    build_epub(
        book_folder,
        tot_chapter_num,
        author_name_full,
        book_name_full,
        lang_alpha2_tag1,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
