from bs4 import BeautifulSoup  # type: ignore
import pytest

from chapter_align.utils.Sentence import Sentence  # type: ignore


@pytest.fixture
def a_sentence() -> Sentence:
    r"""Create a Sentence"""
    sentence_soup = BeautifulSoup("<p>A short sentence.</p>", "html.parser")
    sentence_tag = sentence_soup.find_all("p")[0]
    return Sentence(sentence_tag)


def test_sentence_1_norm(a_sentence: Sentence) -> None:
    r"""Normalize a simple sentence"""
    assert a_sentence.norm_tra == "A short sentence."


def test_sentence_1_len(a_sentence: Sentence) -> None:
    r"""The length is correct"""
    assert a_sentence.len_norm_tra == 17


def test_sentence_1_str(a_sentence: Sentence) -> None:
    r"""The __str__ is correct"""
    assert a_sentence.__str__() == a_sentence.norm_tra


def test_sentence_1_repr(a_sentence: Sentence) -> None:
    r"""The __repr__ does not crash when called"""
    assert isinstance(a_sentence.__repr__(), str)
