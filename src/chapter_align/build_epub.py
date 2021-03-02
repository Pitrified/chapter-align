from pathlib import Path
import logging

# import typing as ty


def build_epub(book_folder: Path) -> None:
    r"""MAKEDOC: what is build_epub doing?"""
    logg = logging.getLogger(f"c.{__name__}.build_epub")
    logg.setLevel("DEBUG")
    logg.debug("Start build_epub")
