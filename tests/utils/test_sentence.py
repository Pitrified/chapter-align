from bs4 import BeautifulSoup  # type: ignore
import pytest

from chapter_align.utils.Sentence import Sentence  # type: ignore


@pytest.fixture
def a_sentence() -> Sentence:
    r"""Create a Sentence"""
    sentence_soup = BeautifulSoup("<p>A short sentence.</p>", "html.parser")
    sentence_tag = sentence_soup.find_all("p")[0]
    return Sentence(sentence_tag)


def test_sentence_norm_1(a_sentence: Sentence) -> None:
    r"""MAKEDOC: what is test_sentence_norm_1 doing?"""
    assert a_sentence.norm_tra == "A short sentence."
