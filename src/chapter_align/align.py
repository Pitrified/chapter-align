from pathlib import Path
import logging
import typing as ty

from .utils.load_chapters import load_chapter


def align_book(
    book_folder: Path,
    languages: ty.Tuple[str, str],
    chapter_templates: ty.Tuple[str, str],
) -> None:
    r"""Align every chapter in a book"""
    logg = logging.getLogger(f"c.{__name__}.align_book")
    logg.setLevel("DEBUG")
    logg.debug("Start align_book")

    chapter_index = 6

    lang_folder0 = book_folder / languages[0]
    load_chapter(lang_folder0, chapter_templates[0], chapter_index)
    # lang_folder1 = book_folder / languages[1]
    # load_chapter(lang_folder1, chapter_templates[1], chapter_index)
