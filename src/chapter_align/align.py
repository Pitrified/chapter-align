from pathlib import Path
import logging

from .utils.load_chapters import load_chapter


def align_book(
    book_folder: Path, language1: str, language2: str, chapter_template: str
) -> None:
    r"""Align every chapter in a book"""
    logg = logging.getLogger(f"c.{__name__}.align_book")
    # logg.setLevel("INFO")
    logg.debug("Start align_book")

    lang_folder1 = book_folder / language1

    chapter_index = 1

    load_chapter(lang_folder1, chapter_template, chapter_index)
