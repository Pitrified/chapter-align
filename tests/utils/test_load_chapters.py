from pathlib import Path

import pytest

from chapter_align.utils.load_chapters import load_chapter  # type: ignore
from chapter_align.utils.misc import get_package_folders  # type: ignore


def test_load_chapter_wrong_path() -> None:
    r"""Fail when the chapter file does not exist"""
    with pytest.raises(FileNotFoundError, match="Chapter not found"):
        wrong_path = Path("definitelynotavalidpathforreal")
        load_chapter(wrong_path, chapter_template="", chapter_index=0)


def test_load_chapter_no_body() -> None:
    r"""Fail when the chapter file does not contain a body"""
    with pytest.raises(RuntimeError, match="Body not found"):
        tests_folder = get_package_folders("tests")
        test_data_folder = tests_folder / "test_data"
        chapter_no_body = "chapter_no_body.xhtml"
        load_chapter(
            test_data_folder, chapter_template=chapter_no_body, chapter_index=0
        )
