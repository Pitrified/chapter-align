from bs4 import BeautifulSoup  # type: ignore
import pytest

from chapter_align.utils.Sentence import Sentence  # type: ignore
from chapter_align.utils.SentenceList import SentenceList  # type: ignore


@pytest.fixture
def a_sentence() -> Sentence:
    r"""Create a Sentence"""
    sentence_soup = BeautifulSoup("<p>A short sentence.</p>", "html.parser")
    sentence_tag = sentence_soup.find_all("p")[0]
    return Sentence(sentence_tag)


@pytest.fixture
def another_sentence() -> Sentence:
    r"""Create another Sentence"""
    sentence_soup = BeautifulSoup("<p>Another short sentence.</p>", "html.parser")
    sentence_tag = sentence_soup.find_all("p")[0]
    return Sentence(sentence_tag)


@pytest.fixture
def a_sentence_list(a_sentence: Sentence, another_sentence: Sentence) -> SentenceList:
    r"""Create a SentenceList"""
    a_sentence_list = SentenceList()
    a_sentence_list.append(a_sentence)
    a_sentence_list.append(another_sentence)
    return a_sentence_list
