from pathlib import Path

import pytest

from chapter_align.utils.load_chapters import load_chapter  # type: ignore
from chapter_align.utils.misc import get_package_folders  # type: ignore


@pytest.fixture
def test_data_folder() -> Path:
    r"""The base test data folder"""
    tests_folder = get_package_folders("tests")
    test_data_folder = tests_folder / "test_data"
    return test_data_folder


def test_load_chapter_wrong_path() -> None:
    r"""Fail when the chapter file does not exist"""
    with pytest.raises(FileNotFoundError, match="Chapter not found"):
        wrong_path = Path("definitelynotavalidpathforreal")
        load_chapter(wrong_path)


def test_load_chapter_no_body(test_data_folder: Path) -> None:
    r"""Fail when the chapter file does not contain a body"""
    with pytest.raises(RuntimeError, match="Body not found"):
        chapter_no_body = "chapter_no_body.xhtml"
        chapter_path = test_data_folder / chapter_no_body
        load_chapter(chapter_path)


def test_load_chapter_01(test_data_folder: Path) -> None:
    r"""Load a sample chapter"""
    chapter_sample = "chapter_sample_01.xhtml"
    chapter_path = test_data_folder / chapter_sample
    sentences = load_chapter(chapter_path)
    assert sentences[0].norm_tra == "A short sentence."
    assert sentences[1].norm_tra == "Another short sentence."
    assert (
        sentences[2].norm_tra
        == "  1. “The Yellow Room”, with its one window and its one door opening into the laboratory."
    )
