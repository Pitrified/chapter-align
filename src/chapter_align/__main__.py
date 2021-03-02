import logging

import click

from . import __version__
from .utils.misc import get_package_folders  # type: ignore
from .utils.misc import setup_logger
from .align import align_book
from .build_epub import build_epub


@click.command()
@click.option(
    "-lld",
    "--log_level_debug",
    type=click.Choice(
        ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="WARN",
    help="Level for the debugging logger",
    show_default=True,
)
@click.option(
    "-llt",
    "--log_level_type",
    type=click.Choice(["anlm", "nlm", "lm", "nm", "m"], case_sensitive=False),
    default="m",
    help="Message format for the debugging logger",
    show_default=True,
)
@click.version_option(version=__version__)
def main(log_level_debug: str, log_level_type: str) -> None:
    r"""The main CLI entry point to the aligner"""
    setup_logger(log_level_debug, log_level_type)
    logg = logging.getLogger(f"c.{__name__}.main")
    logg.debug("Starting main")

    package_root_folder = get_package_folders()
    logg.debug(f"{package_root_folder=}")
    data_folder = package_root_folder / "data"

    # will all be command line args

    author_name_tag = "leroux"
    book_name_tag = "yellow_room"
    book_folder = data_folder / author_name_tag / book_name_tag

    author_name_full = "Gaston Leroux"
    book_name_full = "Le Mystère de la chambre jaune"

    languages = "english", "french"

    # chapter_template0 = "ch_{:04d}_nomap.xhtml"
    chapter_template0 = "ch_{:04d}.xhtml"
    # chapter_template1 = "ch_{:04d}.xhtml"
    chapter_template1 = "main{}.xml"
    chapter_templates = chapter_template0, chapter_template1

    chapter_start_indexes = 1, 0

    tot_chapter_num = 29

    align_book(
        book_folder,
        languages,
        chapter_templates,
        chapter_start_indexes,
        tot_chapter_num,
        author_name_full,
        book_name_full,
    )

    build_epub(
        book_folder,
        tot_chapter_num,
        author_name_full,
        book_name_full,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
