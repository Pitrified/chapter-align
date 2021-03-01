from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore
import pytest

from chapter_align.utils.Sentence import Sentence  # type: ignore
from chapter_align.utils.load_chapters import load_chapter  # type: ignore


@pytest.fixture
def a_sentence() -> Sentence:
    r"""Create a Sentence"""
    sentence_soup = BeautifulSoup("<p>A short sentence.</p>", "html.parser")
    sentence_tag = sentence_soup.find_all("p")[0]
    return Sentence(sentence_tag)


def test_sentence_norm_1(a_sentence: Sentence) -> None:
    r"""MAKEDOC: what is test_sentence_norm_1 doing?"""
    assert a_sentence.norm_tra == "A short sentence."


def test_load_chapter_wrong_path() -> None:
    r"""Fail when the chapter file does not exist"""
    with pytest.raises(FileNotFoundError, match="Chapter not found"):
        wrong_path = Path("definitelynotavalidpathforreal")
        load_chapter(wrong_path, chapter_template="", chapter_index=0)
