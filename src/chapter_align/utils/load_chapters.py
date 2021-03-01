from pathlib import Path
import logging

# from .misc import get_package_root_folder


def load_chapter(lang_folder: Path, chapter_template: str, chapter_index: int) -> None:
    r"""Load a chapter and split it in Sentences"""
    logg = logging.getLogger(f"c.{__name__}.load_chapter")
    # logg.setLevel("INFO")
    logg.debug("Start load_chapter")

    chapter_path = lang_folder / chapter_template.format(chapter_index)
    logg.debug(f"{chapter_path=}")
