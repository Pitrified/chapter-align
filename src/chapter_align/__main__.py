import logging

import click

from . import __version__
from .utils.misc import get_package_folders  # type: ignore
from .utils.misc import setup_logger
from .align import align_book


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

    author_name = "leroux"
    book_name = "yellow_room"
    book_folder = data_folder / author_name / book_name

    languages = "english", "french"
    # chapter_template0 = "ch_{:04d}_nomap.xhtml"
    chapter_template0 = "ch_{:04d}.xhtml"
    chapter_template1 = "ch_{:04d}.xhtml"
    chapter_templates = chapter_template0, chapter_template1

    align_book(book_folder, languages, chapter_templates)


if __name__ == "__main__":  # pragma: no cover
    main()
